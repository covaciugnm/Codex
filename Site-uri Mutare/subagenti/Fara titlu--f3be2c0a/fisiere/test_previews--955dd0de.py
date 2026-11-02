"""Focused preview checks; no browser, network, Docker, or production access."""
import importlib.util
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).parent


class StubResponse:
    def __init__(self, response=None, status=200, mimetype=None):
        self.data = response
        self.status_code = status
        self.mimetype = mimetype
        self.headers = {}


def load_module(name, filename, dependencies):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, dependencies):
        spec.loader.exec_module(module)
    return module


capture = load_module('preview_capture_under_test', 'capture_previews.py', {
    'playwright': types.ModuleType('playwright'),
    'playwright.async_api': types.SimpleNamespace(async_playwright=None),
})
dashboard = load_module('preview_dashboard_under_test', 'domain_dashboard.py', {
    'flask': types.SimpleNamespace(Response=StubResponse),
})


class PreviewTests(unittest.TestCase):
    def test_prefers_working_https_copy_over_http_fallback(self):
        fallback = {'url': 'https://first.example/', 'responds': True,
                    'status': 200, 'https_error': 'TLS failed'}
        healthy = {'url': 'https://second.example/', 'responds': True, 'status': 200}
        row = {'public_url': 'https://public.example/', 'docker': {'links': [fallback, healthy]}}
        self.assertEqual(capture.preferred_copy(row), healthy)

    def test_public_link_is_not_duplicate_copy(self):
        row = {'public_url': 'https://public.example/', 'docker': {'links': [
            {'url': 'https://public.example', 'responds': True, 'status': 200},
        ]}}
        self.assertIsNone(capture.preferred_copy(row))

    def test_targets_reject_credentials_and_non_web_schemes(self):
        urls = ['https://good.example/', 'file:///etc/passwd',
                'https[CREDENTIAL_REDACTED]secret.example/', 'javascript:alert(1)']
        snapshot = {'domains': [{'public_url': url} for url in urls]}
        self.assertEqual(list(capture.capture_targets(snapshot)), [urls[0]])

    def test_traversal_and_arbitrary_filenames_never_read_disk(self):
        preview_path = mock.Mock()
        paths = ['../manifest.json', '../../etc/passwd', '%2e%2e/secret',
                 'manifest.json', 'a.jpg', 'a' * 64 + '.jpg/extra',
                 'a' * 64 + '.jpg\\..\\secret']
        with mock.patch.object(dashboard, 'PREVIEW_PATH', preview_path):
            for suffix in paths:
                with self.subTest(suffix=suffix):
                    response = dashboard.dashboard_response('/_domain-preview/' + suffix)
                    self.assertEqual(response.status_code, 404)
        self.assertEqual(preview_path.mock_calls, [])

    def test_cached_jpeg_serves_and_missing_jpeg_is_404(self):
        with tempfile.TemporaryDirectory() as directory:
            preview_path = pathlib.Path(directory)
            name = 'a' * 64 + '.jpg'
            data = b'\xff\xd8test-jpeg\xff\xd9'
            (preview_path / name).write_bytes(data)
            with mock.patch.object(dashboard, 'PREVIEW_PATH', preview_path):
                response = dashboard.dashboard_response('/_domain-preview/' + name)
                missing = dashboard.dashboard_response('/_domain-preview/' + 'b' * 64 + '.jpg')
            self.assertEqual(response.data, data)
            self.assertEqual(response.mimetype, 'image/jpeg')
            self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
            self.assertEqual(missing.status_code, 404)

    def test_failed_refresh_keeps_previous_image_with_error(self):
        entry = {'status': 'ready', 'image_url': '/_domain-preview/' + 'a' * 64 + '.jpg',
                 'captured_at': '2026-10-20T12:00:00+00:00'}
        capture.unavailable(entry, 'Capture timed out')
        self.assertEqual(entry['status'], 'ready')
        self.assertEqual(entry['captured_at'], '2026-10-20T12:00:00+00:00')
        self.assertEqual(entry['error'], 'Capture timed out')
        self.assertTrue(entry['checked_at'])


if __name__ == '__main__':
    unittest.main()
