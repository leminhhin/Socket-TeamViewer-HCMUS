from ctypes import *

def enable():
    try:
        windll.user32.BlockInput(True) #enable block
        return True
    except:
        return False

def disable():
    try:
        windll.user32.BlockInput(False) #disable block
        return True
    except:
        return False
