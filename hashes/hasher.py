import hashlib
import mimetypes
import os

def identify_file(file_path):
    """
    Returns a dictionary with file identification data: type, size, hashes.
    """
    if not os.path.exists(file_path):
        return None
        
    size = os.path.getsize(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Simple formatting for size
    size_str = f"{size} B"
    if size > 1024 * 1024:
        size_str = f"{size / (1024 * 1024):.2f} MB"
    elif size > 1024:
        size_str = f"{size / 1024:.2f} KB"
    
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
            
    return {
        "file_name": os.path.basename(file_path),
        "type": mime_type or "Unknown",
        "size": size_str,
        "sha256": sha256.hexdigest()
    }
