import os
import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TEST_DIRECTORY = r""

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.changes = []
        
    def on_modified(self, event):
        if not event.is_directory:
            self.changes.append({
                'timestamp': datetime.now().isoformat(),
                'file': event.src_path,
                'action': 'MODIFIED'
            })
            
    def on_created(self, event):
        if not event.is_directory:
            self.changes.append({
                'timestamp': datetime.now().isoformat(),
                'file': event.src_path,
                'action': 'CREATED'
            })
            
    def on_deleted(self, event):
        if not event.is_directory:
            self.changes.append({
                'timestamp': datetime.now().isoformat(),
                'file': event.src_path,
                'action': 'DELETED'
            })

class FileMonitor:
    def __init__(self):
        self.TEST_DIRECTORY = r""
        self.event_handler = FileChangeHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.TEST_DIRECTORY, recursive=False)
        self.observer.start()
        
    def get_monitored_count(self):
        return len(os.listdir(TEST_DIRECTORY))
        
    def get_changes_count(self):
        return len(self.event_handler.changes)
        
    def get_recent_activity(self):
        return self.event_handler.changes[-10:] if self.event_handler.changes else []
