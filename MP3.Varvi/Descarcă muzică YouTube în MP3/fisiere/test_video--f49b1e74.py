import csv
import io
import subprocess
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from PIL import Image
import app
from media_download import convert_media, download_media


class VideoTests(unittest.TestCase):
    def tearDown(self):
        app.jobs.clear(); app.imports.clear()

    def test_real_video_and_audio_from_one_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / 'abcdefghijk.mkv'
            subprocess.run([app.ffmpeg_path(), '-v', 'error', '-f', 'lavfi', '-i', 'color=c=blue:s=160x120:d=1',
                            '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1', '-c:v', 'libx264', '-c:a', 'aac', '-shortest', str(source)], check=True)
            with patch('app.YoutubeDL') as factory:
                ydl = factory.return_value.__enter__.return_value
                info = {'id': 'abcdefghijk', 'title': 'Artist - Piesă'}
                ydl.extract_info.return_value = info; ydl.sanitize_info.return_value = info
                _, _, outputs, errors = download_media(factory, {'ffmpeg_location': app.ffmpeg_path()}, folder,
                    'abcdefghijk', 'https://youtu.be/abcdefghijk', '192', 'both', lambda _: None)
                ydl.extract_info.assert_called_once()
            self.assertFalse(errors)
            self.assertEqual(set(outputs), {'mp3', 'mp4'})
            data = app.metadata(info)
            buffer = io.BytesIO(); Image.new('RGB', (10, 10)).save(buffer, 'JPEG')
            app.write_video_tags(outputs['mp4'], data, buffer.getvalue())
            app.write_tags(outputs['mp3'], data, buffer.getvalue())
            self.assertEqual(MP4(outputs['mp4'])['\xa9nam'], ['Piesă'])
            self.assertGreater(MP4(outputs['mp4']).info.length, .9)
            self.assertEqual(str(MP3(outputs['mp3']).tags['TIT2']), 'Piesă')
            check = subprocess.run([app.ffmpeg_path(), '-i', str(outputs['mp4']), '-f', 'null', '-'], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0)
            self.assertIn('Video: h264', check.stderr)
            self.assertIn('Audio: aac', check.stderr)
            original = outputs['mp4'].read_bytes()
            with self.assertRaises(RuntimeError):
                convert_media(app.ffmpeg_path(), source, outputs['mp4'])
            self.assertEqual(original, outputs['mp4'].read_bytes())

    def test_mode_validation_and_submission_for_both_endpoints(self):
        client = app.app.test_client(); headers = {'X-MP3-App': 'local'}
        for mode in ('mp3', 'mp4', 'both'):
            app.jobs.clear()
            with patch.object(app.pool, 'submit') as submit:
                response = client.post('/api/jobs', json={'url': 'https://youtu.be/abcdefghijk', 'mode': mode}, headers=headers)
                self.assertEqual(response.status_code, 202)
                self.assertEqual(submit.call_args.kwargs['mode'], mode)
            app.jobs.clear(); app.imports['test'] = {'entries': [{}]}
            with patch.object(app.pool, 'submit') as submit:
                response = client.post('/api/imports/test/start', json={'mode': mode}, headers=headers)
                self.assertEqual(response.status_code, 202)
                self.assertEqual(submit.call_args.args[-1], mode)
        for mode in ('bad', None, []):
            self.assertEqual(client.post('/api/jobs', json={'mode': mode}, headers=headers).status_code, 400)
            self.assertEqual(client.post('/api/imports/test/start', json={'mode': mode}, headers=headers).status_code, 400)

    def test_both_files_catalog_and_repeat_collision(self):
        info = {'id': 'abcdefghijk', 'title': 'Artist - Piesă'}
        with tempfile.TemporaryDirectory() as tmp, patch.object(app, 'OUTPUT', Path(tmp)), patch.object(app, 'paced_request', return_value=nullcontext()), patch.object(app, 'YoutubeDL') as factory, patch.object(app, 'write_video_tags'), patch.object(app, 'write_tags'):
            factory.return_value.__enter__.return_value.extract_info.return_value = info
            def fake_download(factory, base, staging, video_id, url, quality, mode, progress):
                outputs = {}
                for ext in ('mp3', 'mp4'):
                    outputs[ext] = staging / ('converted.' + ext)
                    outputs[ext].write_bytes(ext.encode())
                return info, info, outputs, []
            with patch.object(app, 'download_media', side_effect=fake_download):
                for _ in range(2):
                    job = app.new_job()
                    app.run_job(job, 'https://youtu.be/abcdefghijk', '192', mode='both')
                    self.assertEqual(app.jobs[job]['status'], 'done')
                    self.assertEqual(len(app.jobs[job]['files']), 2)
            with (Path(tmp) / 'catalog.csv').open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 4)
            self.assertEqual({r['format'] for r in rows}, {'mp3', 'mp4'})
            self.assertEqual(len({r['file'] for r in rows}), 4)
