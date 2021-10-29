from ctypes import *

def enable():
    windll.user32.BlockInput(True) #enable block
        
def disable():
    windll.user32.BlockInput(False) #disable block
    