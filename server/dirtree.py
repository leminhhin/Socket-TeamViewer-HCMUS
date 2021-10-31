import os
import win32api


def list_files(root):
    data = {'folders': [], 'files': []}
    for item in os.listdir(root):
        path = os.path.join(root, item)
        if os.path.isdir(path):
            data['folders'].append(item)
        else:
            data['files'].append(item)
    return data


def list_drives():
    return [drive.replace('\\', '') for drive in 
        win32api.GetLogicalDriveStrings().split('\000')[:-1]]
    
    
def append_file(filepath, buffer):
    with open(filepath, 'ab') as f:
        f.write(buffer)
        

def read_file(filepath):
    with open(filepath, 'rb') as f:
        while True:
            buffer = f.read(1024)
            if not buffer:
                break
            yield buffer
            
            
def delete_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
