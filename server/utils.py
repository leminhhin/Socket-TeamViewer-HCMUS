import subprocess
import pyautogui


def shutdown():
    #subprocess.Popen('shutdown /s /t 1', shell=True, stdout=subprocess.PIPE)
    # /f: force quit all running apps
    # /s: shutdown
    # /t <number>: time before shutdown 
    subprocess.call(['shutdown', '-f', '-s', '-t', '1'])

def logout():
    # /f: force quit all running apps
    # /l: logout
    # /t <number>: time before logout 
    subprocess.call(['shutdown', '-f', '-l', '-t', '1'])

def get_screenshot():
    return pyautogui.screenshot()