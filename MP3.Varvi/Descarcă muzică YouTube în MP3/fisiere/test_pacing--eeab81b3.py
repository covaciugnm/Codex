import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch
import app


class PacingTests(unittest.TestCase):
    def setUp(self):
        app.jobs.clear()
        self.tmp = tempfile.TemporaryDirectory()
        self.cooldown = patch.object(app, 'COOLDOWN_FILE', Path(self.tmp.name) / 'cooldown.json')
        self.cooldown.start()
        self.job = app.new_job()

    def tearDown(self):
        self.cooldown.stop(); self.tmp.cleanup(); app.jobs.clear()
        app.next_request_at = 0

    def test_countdown_and_spacing_even_on_error(self):
        clock = [100.0]
        app.next_request_at = 103
        with patch.object(app.time, 'monotonic', side_effect=lambda: clock[0]), patch.object(app.time, 'sleep', side_effect=lambda seconds: clock.__setitem__(0, clock[0] + seconds)):
            with self.assertRaises(RuntimeError):
                with app.paced_request(self.job):
                    self.assertEqual(clock[0], 103)
                    raise RuntimeError('Network error')
            self.assertEqual(app.next_request_at, 123)

    def test_cooldown_blocks_both_start_routes_but_not_preview(self):
        self.assertTrue(app.stop_if_limited(self.job, "Sign in to confirm you’re not a bot"))
        self.assertGreater(app.cooldown_remaining(), 1790)
        client = app.app.test_client()
        for path in ['/api/jobs', '/api/imports/test/start']:
            response = client.post(path, json={}, headers={'X-MP3-App': 'local'})
            self.assertEqual(response.status_code, 429)
            self.assertIn('Retry-After', response.headers)
        self.assertEqual(client.post('/api/imports', headers={'X-MP3-App': 'local'}).status_code, 400)
        with patch.object(app.time, 'time', return_value=1e12):
            self.assertEqual(app.cooldown_remaining(), 0)

    def test_batch_stops_on_429_without_trying_next_link(self):
        imported = {'filename': 'test.xlsx', 'sheets': [{'name': 'Jazz', 'skipped': False}], 'entries': [
            {'url': f'https://youtu.be/{video}', 'sheet': 'Jazz', 'row': i, 'values': {}}
            for i, video in enumerate(['abcdefghijk', '12345678901'], 8)]}
        with patch.object(app, 'OUTPUT', Path(self.tmp.name)), patch.object(app, 'paced_request', return_value=nullcontext()), patch.object(app, 'YoutubeDL') as ydl:
            ydl.return_value.__enter__.return_value.extract_info.side_effect = RuntimeError('HTTP Error 429: Too Many Requests')
            app.run_import(self.job, imported, '192')
            self.assertEqual(ydl.return_value.__enter__.return_value.extract_info.call_count, 1)
        self.assertEqual(app.jobs[self.job]['status'], 'failed')
        self.assertIn('30 de minute', app.jobs[self.job]['message'])

    def test_unavailable_video_does_not_trigger_cooldown(self):
        self.assertFalse(app.stop_if_limited(self.job, 'Private video'))
        self.assertEqual(app.cooldown_remaining(), 0)
