"""Separate audio/video download and local conversion functions."""
import subprocess
from pathlib import Path

MODES = {'mp3', 'mp4', 'both'}


def validate_mode(value):
    if not isinstance(value, str) or value not in MODES:
        raise ValueError('Alege MP3, MP4 sau Ambele.')
    return value


def convert_media(ffmpeg, source, target, quality='192'):
    """Create a new local output; never overwrite a destination."""
    if target.exists():
        raise RuntimeError(f'Fișierul există deja: {target.name}')
    args = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-i', str(source)]
    if target.suffix == '.mp3':
        args += ['-map', '0:a:0', '-vn', '-c:a', 'libmp3lame', '-b:a', quality + 'k', '-ar', '44100', '-ac', '2']
    else:
        args += ['-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                 '-pix_fmt', 'yuv420p', '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
                 '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart']
    result = subprocess.run(args + [str(target)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        if target.exists():
            target.unlink()
        raise RuntimeError(f'Conversie {target.suffix[1:].upper()} eșuată: {result.stderr[-1500:]}')


def download_media(ydl_factory, base, staging, video_id, url, quality, mode, progress):
    """Download once; both outputs use the same downloaded video source."""
    validate_mode(mode)
    options = {**base, 'outtmpl': str(staging / '%(id)s.%(ext)s'),
               'writethumbnail': True, 'progress_hooks': [progress]}
    if mode == 'mp3':
        options.update(format='bestaudio/best',
                       postprocessors=[{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': quality}],
                       postprocessor_args={'extractaudio+ffmpeg_o': ['-ar', '44100', '-ac', '2']})
    else:
        options.update(format='bv[height<=1080]+ba/b[height<=1080]', merge_output_format='mkv')
    with ydl_factory(options) as ydl:
        info = ydl.extract_info(url, download=True)
        clean_info = ydl.sanitize_info(info)
    outputs, errors = {}, []
    if mode == 'mp3':
        output = staging / (video_id + '.mp3')
        if not output.exists():
            raise RuntimeError('Conversia nu a produs un fișier MP3.')
        outputs['mp3'] = output
    else:
        sources = [p for p in staging.iterdir() if p.stem == video_id and p.suffix in {'.mkv', '.mp4', '.webm', '.mov', '.flv'}]
        if len(sources) != 1:
            raise RuntimeError('Nu pot identifica fișierul video descărcat.')
        source = sources[0]
        for extension in (['mp4', 'mp3'] if mode == 'both' else ['mp4']):
            target = staging / ('converted.' + extension)
            try:
                convert_media(base['ffmpeg_location'], source, target, quality)
                outputs[extension] = target
            except RuntimeError as exc:
                errors.append(str(exc))
    return info, clean_info, outputs, errors


def write_video_tags(path, data, cover=None):
    from mutagen.mp4 import MP4, MP4Cover
    video = MP4(path)
    for key, atom in [('title', '\xa9nam'), ('artist', '\xa9ART'), ('album', '\xa9alb'),
                      ('album_artist', 'aART'), ('genre', '\xa9gen'), ('release_date', '\xa9day'),
                      ('description', 'desc')]:
        if data.get(key):
            video[atom] = [str(data[key])]
    video['\xa9cmt'] = [data['url']]
    if cover:
        video['covr'] = [MP4Cover(cover, imageformat=MP4Cover.FORMAT_JPEG)]
    video.save()
