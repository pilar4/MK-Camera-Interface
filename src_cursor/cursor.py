import pyautogui
import numpy as np
from playsound import playsound
import threading



class Cursor:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.is_clicking = False
        # active area of the camera (- this precent)
        self.frame_margin_w = 0.2
        self.frame_margin_h = 0.3

        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = True

    def set_margin(self, w, h):
        self.frame_margin_w = w
        self.frame_margin_h = h

    @staticmethod
    def _play_sound_worker():
        """Helper function to play sound in the background."""
        try:
            # Plays the file. No 'os' module needed.
            playsound("src_cursor/selectsound.wav")
        except Exception:
            # If file is missing or something breaks, just ignore it.
            pass

    def move_and_click(self, raw_x, raw_y, handstate, img_w, img_h):

        # define the offsets
        w_offset = self.frame_margin_w * img_w
        h_offset = self.frame_margin_h * img_h

        # map camera coordinates to screen coordinates
        screen_x = np.interp(raw_x, (w_offset, img_w - w_offset), (0, self.screen_w))
        screen_y = np.interp(raw_y, (h_offset, img_h - h_offset), (0, self.screen_h))

        # movement
        if handstate == 1:  # If hand is active (1 or 2)
            pyautogui.moveTo(screen_x, screen_y)

        # clicking
        if handstate == 2:
            if not self.is_clicking:
                pyautogui.click()
                threading.Thread(target=self._play_sound_worker).start()
                self.is_clicking = True
        else:
            self.is_clicking = False