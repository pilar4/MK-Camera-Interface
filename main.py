import cv2
import numpy as np
import pyautogui
import camera_setup
import hand_tracker
from hand_tracker import HandTracker


def main():
    # 1. Setup Camera
    camera_info = camera_setup.camera_setup()
    cap = camera_info[0]
    screen_w = camera_info[1]
    screen_h = camera_info[2]
    if cap is None:
        return

    # 2. Setup Hand Tracker (Creates the class)
    tracker = HandTracker()

    print("System Ready. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            break

        # Flip the image so it acts like a mirror
        img = cv2.flip(img, 1)

        # 3. Use the Tracker
        # We pass the image to the scanner, it draws on it and returns data
        results = tracker.scan_hands(img)

        # 4. Check if we found a hand to do specific logic
        if results.multi_hand_landmarks:
            # Get the first hand detected (since max_hands=1)
            hand_landmarks = results.multi_hand_landmarks[0]

            # --- PARSING THE DATA ---

            # A. Get the RAW coordinates (0.0 to 1.0)
            # Landmark 8 is the Index Finger Tip
            index_tip = hand_landmarks.landmark[8]

            # Landmark 4 is the Thumb Tip
            thumb_tip = hand_landmarks.landmark[4]

            # B. Convert to PIXELS (0 to 1920, etc.)
            # We need the image height (h) and width (w) to do the math
            h, w, _ = img.shape

            idx_x = int(index_tip.x * w)
            idx_y = int(index_tip.y * h)

            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)


            # Hand state logic
            state = HandTracker.fingers_state(hand_landmarks)

            if state == 0:
                print("closed")

            elif state == 1:
                # OPEN HAND → MOVE CURSOR

                # Scale camera coords to screen coords
                screen_x = np.interp(idx_x, (0, w), (0, screen_w))
                screen_y = np.interp(idx_y, (0, h), (0, screen_h))

                pyautogui.moveTo(screen_x, screen_y)
                print("opened")

            elif state == 2:
                print("pinched")

            # Debug visuals
            cv2.circle(img, (idx_x, idx_y), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (thumb_x, thumb_y), 15, (0, 255, 0), cv2.FILLED)

        # 5. Show Image
        cv2.imshow("M&K Interface", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

