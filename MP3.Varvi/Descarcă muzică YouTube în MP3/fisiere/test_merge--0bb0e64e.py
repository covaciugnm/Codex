import io
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from flask import Flask
from mutagen.mp4 import MP4
import app
from video_merge import concatenate_videos, create_merge_blueprint


def make_clips(folder):
    silent = folder / 'clip2.mp4'
    audio = folder / 'clip10.mp4'
    subprocess.run([app.ffmpeg_path(), '-v', 'error', '-f', 'lavfi', '-i', 'color=c=blue:s=120x160:d=0.5', '-c:v', 'libx264', '-y', str(silent)], check=True)
    subprocess.run([app.ffmpeg_path(), '-v', 'error', '-f', 'lavfi', '-i', 'color=c=red:s=160x120:d=0.5',
                    '-f', 'lavfi', '-i', 'sine=frequency=440:duration=0.5', '-c:v', 'libx264', '-c:a', 'aac', '-shortest', '-y', str(audio)], check=True)
    return silent, audio


class MergeTests(unittest.TestCase):
    def test_mixed_video_and_silent_clip_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp); sources = make_clips(folder)
            target = folder / 'joined.mp4'; progress = []
            concatenate_videos(app.ffmpeg_path(), sources, target, folder / 'work', lambda *args: progress.append(args))
            media = MP4(target)
            self.assertGreater(media.info.length, .9)
            self.assertLess(media.info.length, 1.4)
            self.assertEqual(media.info.channels, 2)
            colors = []
            for second in ('0.15', '0.8'):
                result = subprocess.run([app.ffmpeg_path(), '-v', 'error', '-ss', second, '-i', str(target),
                                         '-frames:v', '1', '-vf', 'crop=100:100,scale=1:1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
                colors.append(result.stdout)
            self.assertGreater(colors[0][2], colors[0][0] + 100)
            self.assertGreater(colors[1][0], colors[1][2] + 100)
            self.assertTrue(all(p.exists() for p in sources))
            with self.assertRaises(ValueError):
                concatenate_videos(app.ffmpeg_path(), sources, target, folder / 'work', lambda *args: None)

    def test_upload_start_result_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); sources = make_clips(root)
            testapp = Flask('merge-test')
            testapp.register_blueprint(create_merge_blueprint(root/'downloads', root/'runtime', app.ffmpeg_path))
            client = testapp.test_client(); ids = []
            for path in sources:
                response = client.post('/api/merge/uploads', data={'file':(io.BytesIO(path.read_bytes()),path.name)})
                self.assertEqual(response.status_code, 201); ids.append(response.json['id'])
            self.assertEqual(client.post('/api/merge/jobs', json={'ids':ids[:1]}).status_code, 400)
            response = client.post('/api/merge/jobs', json={'ids':ids, 'name':'../Test'})
            self.assertEqual(response.status_code, 202)
            job = response.json['id']; status = None
            deadline = time.monotonic() + 45
            while time.monotonic() < deadline:
                status = client.get('/api/merge/jobs/'+job).json
                if status['status'] in ('done','failed'): break
                time.sleep(.1)
            self.assertEqual(status['status'], 'done', status)
            target = root/'downloads'/status['file']
            self.assertTrue(target.is_file())
            self.assertTrue(target.resolve().is_relative_to((root/'downloads').resolve()))
            self.assertEqual(list((root/'runtime'/'merge-uploads').iterdir()), [])
            self.assertEqual(client.post('/api/merge/jobs', json={'ids':ids}).status_code, 400)

    def test_reject_nonvideo_upload_and_bad_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            testapp = Flask('merge-errors')
            testapp.register_blueprint(create_merge_blueprint(Path(tmp)/'out', Path(tmp)/'work', app.ffmpeg_path))
            client = testapp.test_client()
            self.assertEqual(client.post('/api/merge/uploads', data={'file':(io.BytesIO(b'abc'),'a.txt')}).status_code,400)
            self.assertEqual(client.post('/api/merge/uploads', data={'file':(io.BytesIO(b''),'a.mp4')}).status_code,400)
            for payload in ({'ids':['unknown','unknown']},{'ids':['a','b']}, {'ids':[{},{}]}, []):
                self.assertEqual(client.post('/api/merge/jobs',json=payload).status_code,400)

    def test_invalid_video_not_published(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); fake = root/'fake.mp4';fake.write_bytes(b'not a movie')
            with self.assertRaises(ValueError):
                concatenate_videos(app.ffmpeg_path(),[fake,fake],root/'out.mp4',root/'work',lambda *args:None)
            self.assertFalse((root/'out.mp4').exists())
