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
    

