from flask import Blueprint, jsonify, request
from datetime import datetime
import os
import hashlib
from notifier import EmailNotifier


api_bp = Blueprint('api', __name__)
TEST_DIRECTORY = r"C:\\Users\\eucli\\OneDrive\\Desktop\\testing"
file_hashes = {}
email_notifier = EmailNotifier()
previous_files = set()
first_run = True  

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    stats = {
        'filesMonitored': 156,  # We'll connect this with real data later
        'changesDetected': 3,
        'lastScan': datetime.now().isoformat(),
        'recentActivity': [
            {
                'timestamp': datetime.now().isoformat(),
                'file': 'C:\\Windows\\System32\\drivers\\etc\\hosts',
                'action': 'MODIFIED',
                'riskScore': 75
            }
        ]
    }
    return jsonify(stats)

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

@api_bp.route('/files', methods=['GET'])
def get_files():
    global previous_files, first_run
    files = {
        'monitored': [],
        'total': 0,
        'changes': []
    }
    
    current_files = set()
    
    for filename in os.listdir(TEST_DIRECTORY):
        file_path = os.path.join(TEST_DIRECTORY, filename)
        current_files.add(file_path)
        
        if os.path.isfile(file_path):
            current_hash = get_file_hash(file_path)
            
            # Skip alerts on first run
            if first_run:
                status = "UNCHANGED"
                file_hashes[file_path] = current_hash
            else:
                # Normal change detection logic
                if file_path not in file_hashes:
                    status = "NEW"
                    email_notifier.send_alert(f"New file detected: {file_path}")
                elif file_hashes[file_path] != current_hash:
                    status = "CHANGED"
                    email_notifier.send_alert(f"File modified: {file_path}")
                else:
                    status = "UNCHANGED"
                    
                file_hashes[file_path] = current_hash
            
            files['monitored'].append({
                'path': file_path,
                'lastModified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                'status': status,
                'hash': current_hash
            })
    
    if not first_run:
        # Detect deleted files only after first run
        deleted_files = previous_files - current_files
        if deleted_files:
            for file_path in deleted_files:
                email_notifier.send_alert(f"File deleted: {file_path}")
    
    previous_files = current_files
    files['total'] = len(files['monitored'])
    
    if first_run:
        first_run = False
        print("Initial baseline created!")
    
    return jsonify(files)


@api_bp.route('/alerts', methods=['GET'])
def get_alerts():
    alerts = [
        {
            'id': 1,
            'timestamp': datetime.now().isoformat(),
            'severity': 'HIGH',
            'message': 'Critical system file modified',
            'file': 'C:\\Windows\\System32\\kernel32.dll'
        }
    ]
    return jsonify(alerts)

@api_bp.route('/system-health', methods=['GET'])
def get_system_health():
    health = {
        'status': 'HEALTHY',
        'lastCheckTime': datetime.now().isoformat(),
        'metrics': {
            'cpu': 45,
            'memory': 68,
            'diskSpace': 72
        }
    }
    return jsonify(health)
