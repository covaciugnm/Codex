import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from mutagen.id3 import ID3
import app


class AppTests(unittest.TestCase):
    def test_url_validation(self):
        self.assertEqual(app.youtube_url('https://youtu.be/abcdefghijk?t=5'), 'https://www.youtube.com/watch?v=abcdefghijk')
        self.assertIn('playlist?list=', app.youtube_url('https://www.youtube.com/watch?v=abcdefghijk&list=PL123456789012'))
        for url in ['http://127.0.0.1/', 'https://youtube.com.evil.com/watch?v=abcdefghijk', 'file:///etc/passwd', 'https://youtube.com/@channel']:
            with self.assertRaises(ValueError):
                app.youtube_url(url)

    def test_artist_and_album_provenance(self):
        data = app.metadata({'id': 'abcdefghijk', 'title': 'Cântăreț - Piesă (Official)', 'upload_date': '20261008'}, 'Colecție', 2)
        self.assertEqual(data['artist'], 'Cântăreț')
        self.assertEqual(data['title'], 'Piesă (Official)')
        self.assertEqual(data['release_date'], '')
        self.assertEqual(data['album_source'], 'playlist')
        unknown = app.metadata({'id': 'abcdefghijk', 'title': 'Piesă', 'uploader': 'Un canal'})
        self.assertEqual(unknown['artist'], 'Artist necunoscut')
        official = app.metadata({'id': 'abcdefghijk', 'title': 'Video', 'artist': 'Artist real', 'track': 'Piesa reală', 'album': 'Album'})
        self.assertEqual(official['title'], 'Piesa reală')
        self.assertEqual(official['artist_source'], 'YouTube: artist')

    def test_tags_and_catalog_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'audio.mp3'
            path.write_bytes(b'')
            data = app.metadata({'id': 'abcdefghijk', 'title': 'Ștefan - Cântec', 'description': 'Descriere', 'release_date': '20250102'})
            data['file'] = 'folder/audio.mp3'
            app.write_tags(path, data, b'jpeg-test')
            tags = ID3(path)
            self.assertEqual(tags.version, (2, 3, 0))
            self.assertEqual(str(tags['TPE1']), 'Ștefan')
            self.assertEqual(str(tags['TIT2']), 'Cântec')
            self.assertEqual(tags.getall('APIC')[0].mime, 'image/jpeg')
            data['description'] = '=DANGER()'
            catalog = Path(tmp) / 'catalog.csv'
            app.write_catalog(catalog, data)
            app.write_catalog(catalog, data)
            with catalog.open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['description'], "'=DANGER()")

    def test_local_api_and_path_safety(self):
        client = app.app.test_client()
        self.assertEqual(client.get('/').status_code, 200)
        self.assertEqual(client.get('/', headers={'Host': 'evil.example'}).status_code, 403)
        self.assertEqual(client.post('/api/jobs', json={'url': 'https://youtu.be/abcdefghijk'}).status_code, 403)
        self.assertEqual(client.post('/api/jobs', json={'url': 'bad'}, headers={'X-MP3-App': 'local'}).status_code, 400)
        self.assertEqual(client.get('/files/../app.py').status_code, 404)
        self.assertEqual(app.safe_name('CON'), '_CON')
        self.assertNotIn('/', app.safe_name('../a/b'))


if __name__ == '__main__':
    unittest.main()
