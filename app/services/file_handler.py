# Handles File I/O. Reads uploaded text files to be indexed. (temporary)

import os

def save_and_read_file(file_content: bytes, filename: str):
    temp_path = f"temp_{filename}"
    with open(temp_path, "wb") as f:
        f.write(file_content)
    
    with open(temp_path, "r") as f:
        data = f.read()
    
    os.remove(temp_path)
    return data