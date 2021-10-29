import os
import winreg
import subprocess
import shutil

type_str2code = {
    'String'                : winreg.REG_SZ,
    'Binary'                : winreg.REG_BINARY,
    'DWORD'                 : winreg.REG_DWORD,
    'QWORD'                 : winreg.REG_QWORD,
    'Multi-String'          : winreg.REG_MULTI_SZ,
    'Expandable String'     : winreg.REG_EXPAND_SZ
}

type_code2str = {
    winreg.REG_SZ           : 'String',
    winreg.REG_BINARY       : 'Binary',
    winreg.REG_DWORD        : 'DWORD',
    winreg.REG_QWORD        : 'QWORD',
    winreg.REG_MULTI_SZ     : 'Multi-String',
    winreg.REG_EXPAND_SZ    : 'Expandable String'
}

def _get_key_object(key_path, access_right=winreg.KEY_READ): # Raises an exception if not successful
    pos = key_path.rfind('/')
    if pos == -1:
        return getattr(winreg, key_path)
    key = _get_key_object(key_path[:pos])
    return winreg.OpenKey(key, key_path[pos+1:], access=access_right)


def get_value(key_path, value_name):
    key = _get_key_object(key_path)
    idx = 0
    while True:
        name, value, dtype = winreg.EnumValue(key, idx)
        idx += 1
        if name == value_name:
            return {'value':value, 'dtype':type_code2str[dtype]}
    

def set_value(key_path, value_name, dtype, value):
    key = _get_key_object(key_path, access_right=winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, value_name, 0, type_str2code[dtype], value)
    

def delete_value(key_path, value_name):
    key = _get_key_object(key_path, access_right=winreg.KEY_SET_VALUE)
    winreg.DeleteValue(key, value_name)


def create_key(key_path):
    pos = key_path.rfind('/')
    if pos == -1:
        raise Exception()
    key = _get_key_object(key_path[:pos])
    winreg.CreateKey(key, key_path[pos+1:])


def delete_key(key_path):
    key = _get_key_object(key_path)
    winreg.DeleteKey(key, '')


def import_reg(content):
    with open('temp.reg', 'w') as f:
        f.write(content)
    proc = subprocess.Popen('reg import temp.reg', shell=True, stdout=subprocess.PIPE)
    os.remove('temp.reg')
