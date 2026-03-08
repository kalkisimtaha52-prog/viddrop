import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

import shutil

if os.name == 'nt':
    FFMPEG_PATH = os.path.join(BASE_DIR, "ffmpeg.exe")
else:
    # Try to find ffmpeg in system path (e.g. /opt/homebrew/bin/ffmpeg)
    system_ffmpeg = shutil.which("ffmpeg")
    FFMPEG_PATH = system_ffmpeg if system_ffmpeg else "ffmpeg"

progress_store = {}

def get_ydl_opts(quality, task_id):
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            percent = int((downloaded / total) * 100) if total > 0 else 0
            progress_store[task_id] = {
                'status': 'downloading',
                'percent': percent,
                'speed': d.get('_speed_str', '...'),
                'eta': d.get('_eta_str', '...')
            }
        elif d['status'] == 'finished':
            progress_store[task_id] = {'status': 'processing', 'percent': 99}

    quality_map = {
        '4k':    'bestvideo[height<=2160][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best',
        '1080p': 'bestvideo[height<=1080][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best',
        '720p':  'bestvideo[height<=720][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best',
        '480p':  'bestvideo[height<=480][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best',
        '360p':  'bestvideo[height<=360][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo[height<=360]+bestaudio/best',
        'audio': 'bestaudio[ext=m4a]/bestaudio/best',
    }

    opts = {
        'format': quality_map.get(quality, quality_map['1080p']),
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'noplaylist': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'ffmpeg_location': FFMPEG_PATH,
        'merge_output_format': 'mp4',
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            },
            {
                'key': 'FFmpegMetadata',
            }
        ],
    }

    if quality == 'audio':
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }]
        opts.pop('merge_output_format', None)

    return opts
