import subprocess
import pyautogui


def shutdown():
    subprocess.Popen('shutdown /s /t 1', shell=True, stdout=subprocess.PIPE)
        

def logout():
    try:
        subprocess.Popen('shutdown /l /t 1', shell=True, stdout=subprocess.PIPE)
        return True
    except:
        return False

def get_screenshot():
    return pyautogui.screenshot()