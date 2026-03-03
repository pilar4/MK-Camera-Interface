import pyautogui
import numpy as np
from playsound import playsound
import threading
import time
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    import cursor_cpp
except ImportError:
    print("\nCRITICAL ERROR: Could not import 'cursor_cpp'.")
    print(f"Make sure the .pyd file is located in: {current_dir}\n")
    sys.exit(1)


class Cursor:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.is_clicking = False
        self.frame_margin_w = 0.2
        self.frame_margin_h = 0.3
        self.last_handstate = None
        self.has_synced = False
        self.w_sens_ratio = 0.1  # precent from edge
        self.h_sens_ratio = 0.1

        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False

        self.physics = cursor_cpp.CursorPhysics(screen_w=screen_w, screen_h=screen_h)

        self.last_time = time.time()
        self.prev_s_x = None
        self.prev_s_y = None


    @staticmethod
    def _play_sound_worker():
        try:
            playsound(os.path.join(current_dir, "selectsound.wav"))
        except Exception:
            pass


    def move_and_click(self, raw_x, raw_y, handstate, img_w, img_h):

        w_offset = img_w * self.w_sens_ratio
        h_offset = img_h * self.h_sens_ratio

        screen_x = np.interp(raw_x, (w_offset, img_w - w_offset), (0, self.screen_w))
        screen_y = np.interp(raw_y, (h_offset, img_h - h_offset), (0, self.screen_h))

        # movement
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        dt = min(dt, 0.03)  # safety clamp

        if handstate == 1:
            if self.prev_s_x is None or not self.has_synced:
                self.prev_s_x = screen_x
                self.prev_s_y = screen_y

                if not self.has_synced:
                    self.physics.reset(screen_x, screen_y)
                    self.has_synced = True
                else:
                    self.physics.unclutch()

                self.last_handstate = handstate
                return

            dx = screen_x - self.prev_s_x
            dy = screen_y - self.prev_s_y

            if abs(dx) < 5 and abs(dy) < 5:
                dx = dy = 0.0

            true_x, true_y = self.physics.update(dx, dy, dt)
            pyautogui.moveTo(true_x, true_y)

            self.prev_s_x = screen_x
            self.prev_s_y = screen_y

        else:
            if self.last_handstate == 1:
                self.physics.clutch()
            self.prev_s_x = None
            self.prev_s_y = None

        if handstate == 2:
            if not self.is_clicking:
                pyautogui.click()
                threading.Thread(target=self._play_sound_worker).start()
                self.is_clicking = True
        else:
            self.is_clicking = False

        self.last_handstate = handstate

