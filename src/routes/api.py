from flask import Blueprint, request, jsonify, send_file
import yt_dlp
import os
import threading
import uuid
from src.services.downloader import get_ydl_opts, progress_store

api_bp = Blueprint('api', __name__)

@api_bp.route('/info', methods=['POST'])
def get_info():
    data = request.json
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'error': 'URL gerekli'}), 400
    try:
        info_opts = {
            'quiet': True, 
            'noplaylist': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
        }
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title', 'Bilinmiyor'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'channel': info.get('uploader', 'Bilinmiyor'),
                'view_count': info.get('view_count', 0),
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/download', methods=['POST'])
def start_download():

    data = request.json
    url = data.get('url', '').strip()
    quality = data.get('quality', '1080p')
    if not url:
        return jsonify({'error': 'URL gerekli'}), 400

    import time
    task_id = str(uuid.uuid4())
    progress_store[task_id] = {
        'status': 'starting', 
        'percent': 0,
        'created_at': time.time()
    }

    def run():
        try:
            opts = get_ydl_opts(quality, task_id)
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if quality != 'audio':
                    filename = os.path.splitext(filename)[0] + '.mp4'
                progress_store[task_id] = {
                    'status': 'done',
                    'percent': 100,
                    'filename': os.path.basename(filename),
                    'filepath': filename,
                    'created_at': time.time()
                }
        except Exception as e:
            progress_store[task_id] = {'status': 'error', 'error': str(e), 'created_at': time.time()}

    threading.Thread(target=run, daemon=True).start()
    return jsonify({'task_id': task_id})


@api_bp.route('/progress/<task_id>')
def get_progress(task_id):
    return jsonify(progress_store.get(task_id, {'status': 'not_found'}))


@api_bp.route('/file/<task_id>')
def get_file(task_id):
    task = progress_store.get(task_id)
    if not task or task.get('status') != 'done':
        return jsonify({'error': 'Dosya hazır değil'}), 404
    filepath = task.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'Dosya bulunamadı'}), 404
    return send_file(filepath, as_attachment=True)
