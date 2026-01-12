import pyautogui

class Cursor:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.state = 0
        pyautogui.PAUSE = 0

    def update(self, x, y, handstate):
        """Updates the internal position."""
        self.pos_x = x
        self.pos_y = y
        self.state = handstate