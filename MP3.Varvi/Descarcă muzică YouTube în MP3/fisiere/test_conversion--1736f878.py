import subprocess
import tempfile
import unittest
from pathlib import Path
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.ffmpeg import FFmpegExtractAudioPP
import app


class ConversionTests(unittest.TestCase):
    def test_real_conversion_with_installed_ffmpeg(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'sample.wav'
            subprocess.run([app.ffmpeg_path(), '-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1', str(source)], check=True, capture_output=True)
            with YoutubeDL({'quiet': True, 'ffmpeg_location': app.ffmpeg_path(), 'postprocessor_args': {'extractaudio+ffmpeg_o': ['-ar', '44100', '-ac', '2']}}) as ydl:
                processor = FFmpegExtractAudioPP(ydl, preferredcodec='mp3', preferredquality='192')
                _, result = processor.run({'filepath': str(source), 'ext': 'wav'})
            output = Path(result['filepath'])
            app.write_tags(output, app.metadata({'id': 'abcdefghijk', 'title': 'Artist - Piesă'}))
            audio = MP3(output)
            self.assertEqual(audio.info.sample_rate, 44100)
            self.assertEqual(audio.info.channels, 2)
            self.assertGreater(audio.info.length, 0.9)
            self.assertEqual(str(audio.tags['TIT2']), 'Piesă')
