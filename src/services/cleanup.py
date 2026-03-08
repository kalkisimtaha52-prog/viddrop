import os
import time
import threading
from src.services.downloader import progress_store, DOWNLOAD_DIR

CLEANUP_AGE_SECONDS = 3600

def cleanup_old_tasks():
    while True:
        try:
            current_time = time.time()
            tasks_to_delete = []

            for task_id, task in progress_store.items():
                if current_time - task.get('created_at', current_time) > CLEANUP_AGE_SECONDS:
                    tasks_to_delete.append(task_id)
            
            for task_id in tasks_to_delete:
                task = progress_store.pop(task_id, None)
                if task and 'filepath' in task and task['filepath']:
                    try:
                        if os.path.exists(task['filepath']):
                            os.remove(task['filepath'])
                    except Exception as e:
                        print(f"Error deleting file {task['filepath']}: {e}")
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        try:
            if os.path.exists(DOWNLOAD_DIR):
                for filename in os.listdir(DOWNLOAD_DIR):
                    filepath = os.path.join(DOWNLOAD_DIR, filename)
                    if os.path.isfile(filepath):
                        file_age = current_time - os.path.getmtime(filepath)
                        if file_age > CLEANUP_AGE_SECONDS:
                            try:
                                os.remove(filepath)
                            except Exception as e:
                                print(f"Error deleting untracked file {filepath}: {e}")
        except Exception as e:
            print(f"Error during untracked cleanup: {e}")

        time.sleep(1800)

def start_cleanup_thread():
    # Only start thread if not in serverless environment
    if not os.environ.get('VERCEL'):
        threading.Thread(target=cleanup_old_tasks, daemon=True).start()
