import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self):
        """
        Initialize the MediaPipe Hands model once.
        """
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        # Configure the model
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )

    def scan_hands(self, img):
        """
        Takes an image frame, finds hands, draws the skeleton,
        and returns the results.
        """
        # 1. Convert BGR (OpenCV) to RGB (MediaPipe)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 2. Process the frame (The heavy AI work)
        results = self.hands.process(img_rgb)

        # 3. Draw landmarks on the original image if found
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return results