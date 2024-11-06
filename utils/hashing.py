from typing import BinaryIO
import hashlib

def generate_file_id(file: BinaryIO) -> str:
    hash_md5 = hashlib.md5()
    
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    
    file.seek(0)
    
    return hash_md5.hexdigest()