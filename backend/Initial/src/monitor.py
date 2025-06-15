import json
import time
from datetime import datetime
from pathlib import Path
from hash_utils import HashManager
from notifier import EmailNotifier
import logging

class FileMonitor:
    def __init__(self):
        # Get project root directory
        project_root = Path(__file__).parent.parent
        
        # Setup logging
        logging.basicConfig(
            filename=str(project_root / "logs" / "fim.log"),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Load configuration
        config_path = project_root / "config" / "config.json"
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Initialize components
        self.hash_manager = HashManager(str(project_root / "json-hash"), self.config)
        self.notifier = EmailNotifier()
        self.scan_interval = self.config["scan_interval"]
        
        # Generate initial baseline
        initial_hashes = self.hash_manager.initialize_baseline()


    def scan_files(self):
        """Scan all monitored directories and generate hashes."""
        current_hashes = {}
        
        for directory in self.config["directories_to_monitor"]:
            try:
                path = Path(directory)
                if path.exists():
                    for file_path in path.rglob("*"):
                        if file_path.is_file():
                            hash_info = self.hash_manager.generate_file_hash(str(file_path))
                            if hash_info:
                                current_hashes[str(file_path)] = hash_info
            except Exception as e:
                logging.error(f"Error scanning directory {directory}: {str(e)}")
        
        return current_hashes

    def detect_changes(self, old_hashes, new_hashes):
        """Compare old and new hashes to detect changes."""
        changes = {}
        
        # Check for modified or new files
        for file_path, new_hash_info in new_hashes.items():
            if file_path in old_hashes:
                if new_hash_info["hash"] != old_hashes[file_path]["hash"]:
                    changes[file_path] = {
                        "old_hash": old_hashes[file_path]["hash"],
                        "new_hash": new_hash_info["hash"],
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                changes[file_path] = {
                    "old_hash": None,
                    "new_hash": new_hash_info["hash"],
                    "timestamp": datetime.now().isoformat()
                }
        
        # Check for deleted files
        for file_path in old_hashes:
            if file_path not in new_hashes:
                changes[file_path] = {
                    "old_hash": old_hashes[file_path]["hash"],
                    "new_hash": None,
                    "timestamp": datetime.now().isoformat()
                }
        
        return changes

    def run(self):
        """Main monitoring loop."""
        logging.info("File Integrity Monitoring started")
        
        while True:
            try:
                # Load previous hashes
                old_hashes = self.hash_manager.load_hashes()
                
                # Scan current files
                new_hashes = self.scan_files()
                
                # Detect changes
                changes = self.detect_changes(old_hashes, new_hashes)
                
                if changes:
                    logging.info(f"Changes detected: {len(changes)} files affected")
                    self.notifier.send_alert(changes)
                    self.hash_manager.save_hashes(new_hashes)
                
                time.sleep(self.scan_interval)
                
            except Exception as e:
                logging.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(60)  # Wait before retrying

    def run(self):
        """Main monitoring loop."""
        print("FIM System Started - Monitoring files...")
        logging.info("File Integrity Monitoring started")
        
        while True:
            try:
                print("Scanning files...")
                # Load previous hashes
                old_hashes = self.hash_manager.load_hashes()
                
                # Scan current files
                new_hashes = self.scan_files()
                print(f"Monitoring {len(new_hashes)} files")
                
                # Detect changes
                changes = self.detect_changes(old_hashes, new_hashes)
                
                if changes:
                    print("Changes detected! Sending alert...")
                    logging.info(f"Changes detected: {len(changes)} files affected")
                    self.notifier.send_alert(changes)
                    self.hash_manager.save_hashes(new_hashes)
                else:
                    print("No changes detected")
                
                print(f"Waiting {self.scan_interval} seconds before next scan...")
                time.sleep(self.scan_interval)
                
            except Exception as e:
                logging.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(30)

