from pynput.keyboard import Listener

class KeystrokeDetector:
    def __init__(self):
        self.keys = ''
        self.hooked = False
        
    def on_press(self, key):
        if not self.hooked:
            return False
        try:
            self.keys += key.char + ' '
        except AttributeError:
            self.keys += (' ' + format(key) + ' ')

    def start_listening(self):
        self.keys = ''
        self.hooked = True
        listener = Listener(on_press=self.on_press)
        listener.start()

    def end_listening(self):
        self.hooked = False

    def get_keys(self):
        key = self.keys
        self.keys = ''
        return key
