import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

class HashManager:
    def __init__(self, json_dir="json-hash", config=None):
        self.json_dir = Path(json_dir)
        self.json_dir.mkdir(exist_ok=True)
        self.hash_file = self.json_dir / "file_hashes.json"
        self.config = config


    def generate_file_hash(self, file_path):
        """Generate SHA-256 hash for a given file."""
        try:
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for block in iter(lambda: f.read(4096), b""):
                    sha256.update(block)
            return {
                "hash": sha256.hexdigest(),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "size": os.path.getsize(file_path)
            }
        except (IOError, PermissionError) as e:
            return None

    def save_hashes(self, hash_dict):
        """Save hashes to JSON file."""
        with open(self.hash_file, "w") as f:
            json.dump(hash_dict, f, indent=4)

    def load_hashes(self):
        """Load hashes from JSON file."""
        if self.hash_file.exists():
            with open(self.hash_file, "r") as f:
                return json.load(f)
        return {}
    
    def initialize_baseline(self):
        """Generate initial baseline hashes"""
        print("Generating initial baseline hashes...")
        current_hashes = {}
        for directory in self.config["directories_to_monitor"]:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    hash_info = self.generate_file_hash(file_path)
                    if hash_info:
                        current_hashes[file_path] = hash_info
        
        self.save_hashes(current_hashes)
        print(f"Baseline created - {len(current_hashes)} files indexed")
        return current_hashes

