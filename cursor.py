import pyautogui
import numpy as np


class Cursor:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h

        # Flag to prevent infinite clicking
        self.is_clicking = False

        # Configuration for the active area of the camera
        self.frame_margin_w = 0.2  # 20%
        self.frame_margin_h = 0.3  # 30%

        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = True

    def move_and_click(self, raw_x, raw_y, handstate, img_w, img_h):
        """
        Calculates screen coordinates and performs mouse actions.
        raw_x, raw_y: The coordinates from the webcam (index finger)
        img_w, img_h: The dimensions of the webcam image
        """

        # 1. Define the active zone offsets based on image size
        w_offset = self.frame_margin_w * img_w
        h_offset = self.frame_margin_h * img_h

        # 2. Map Camera Coordinates to Screen Coordinates
        # using np.interp to scale the movement
        screen_x = np.interp(raw_x, (w_offset, img_w - w_offset), (0, self.screen_w))
        screen_y = np.interp(raw_y, (h_offset, img_h - h_offset), (0, self.screen_h))

        # 3. Handle Movement
        if handstate == 1:  # If hand is active (1 or 2)
            pyautogui.moveTo(screen_x, screen_y)

        # 4. Handle Clicking (The Flag Logic)
        if handstate == 2:
            # Only click if we haven't clicked already
            if not self.is_clicking:
                pyautogui.click()
                self.is_clicking = True
        else:
            # Reset the flag so we can click again later
            self.is_clicking = False