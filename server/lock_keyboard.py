import keyboard
from time import sleep
import threading

def enable():
    t1 = threading.Thread(target=block_input_start)
    t1.start()

def disable():
    block_input_stop()
    
def block_input_start():
    for i in range(150):
        keyboard.block_key(i)

def block_input_stop():
    for i in range(150):
        keyboard.unblock_key(i)