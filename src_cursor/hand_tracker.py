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
        ring_up = HandTracker._finger_extended(hand_landmarks, 16)
        pinky_up = HandTracker._finger_extended(hand_landmarks, 20)

        not_fist = middle_up or ring_up or pinky_up

        if pinch_close and not_fist:
            return 2

        # ---------- OPEN / CLOSED ----------
        pinky_dist = math.dist(
            (hand_landmarks.landmark[20].x, hand_landmarks.landmark[20].y),
            (hand_landmarks.landmark[17].x, hand_landmarks.landmark[17].y)
        )
        ring_dist = math.dist(
            (hand_landmarks.landmark[16].x, hand_landmarks.landmark[16].y),
            (hand_landmarks.landmark[13].x, hand_landmarks.landmark[13].y)
        )
        middle_dist = math.dist(
            (hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y),
            (hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y)
        )

        hand_sideways = math.dist(
            (hand_landmarks.landmark[6].x, hand_landmarks.landmark[6].y),
            (hand_landmarks.landmark[19].x, hand_landmarks.landmark[19].y)
        )

        pinky_ratio = pinky_dist / hand_scale
        ring_ratio = ring_dist / hand_scale
        middle_ratio = middle_dist / hand_scale


        closed_threshold = 0.5

        if (
                sum([
                    pinky_ratio < closed_threshold,
                    ring_ratio < closed_threshold,
                    middle_ratio < closed_threshold
                ]) >= 2
                or hand_sideways > 100
        ):
            return 0

        return 1
