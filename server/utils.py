import subprocess
import pyautogui


def shutdown():
    subprocess.Popen('shutdown /s /t 1', shell=True, stdout=subprocess.PIPE)
        

def logout():
    subprocess.Popen('shutdown /l /t 1', shell=True, stdout=subprocess.PIPE)

def get_screenshot():
    return pyautogui.screenshot()