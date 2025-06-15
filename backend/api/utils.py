import hashlib
import os

def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_file_info(filepath):
    """Get file information"""
    return {
        'path': filepath,
        'size': os.path.getsize(filepath),
        'lastModified': os.path.getmtime(filepath),
        'hash': calculate_file_hash(filepath)
    }

