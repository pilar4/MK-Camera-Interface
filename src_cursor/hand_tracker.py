import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )

    def scan_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return results


    @staticmethod
    def _finger_extended(hand, tip):
        return hand.landmark[tip].y < hand.landmark[tip - 2].y

    @staticmethod
    def fingers_state(hand_landmarks):
        # 0 - closed
        # 1 - opened
        # 2 - pinch

        # ---------- PINCH ----------
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        wrist = hand_landmarks.landmark[0]
        middle_mcp = hand_landmarks.landmark[9]

        pinch_dist = math.dist((thumb.x, thumb.y), (index.x, index.y))
        hand_scale = math.dist((wrist.x, wrist.y), (middle_mcp.x, middle_mcp.y))

        pinch_close = pinch_dist / hand_scale < 0.35

        middle_up = HandTracker._finger_extended(hand_landmarks, 12)
        ring_up   = HandTracker._finger_extended(hand_landmarks, 16)
        pinky_up  = HandTracker._finger_extended(hand_landmarks, 20)

        not_fist = middle_up or ring_up or pinky_up

        if pinch_close and not_fist:
            return 2

        # ---------- OPEN / CLOSED ----------
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[20].x:
            if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
                return 0
        else:
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                return 0

        # skips index for quality, but we will se if its necessary
        for tip in [12, 16, 20]:
            if not HandTracker._finger_extended(hand_landmarks, tip):
                return 0

        return 1
