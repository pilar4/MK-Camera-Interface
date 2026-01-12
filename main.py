import cv2
import numpy as np
import pyautogui
import camera_setup
from cursor import Cursor
from hand_tracker import HandTracker


def main():

    """SETUP"""
    # Camera
    camera_info = camera_setup.camera_setup()
    cap = camera_info[0]
    screen_w = camera_info[1]
    screen_h = camera_info[2]

    if cap is None:
        return

    # Hand Tracker
    tracker = HandTracker()
    print("System Ready. Press 'q' to quit.")

    # Cursor
    cursor = Cursor()




    while True:

        success, img = cap.read()
        if not success:
            break

        # Mirror image
        img = cv2.flip(img, 1)

        # 3. Scan hands
        results = tracker.scan_hands(img)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Get landmarks
            index_tip = hand_landmarks.landmark[8]   # Index finger tip
            thumb_tip = hand_landmarks.landmark[4]   # Thumb tip

            # Image size
            h, w, _ = img.shape
            # Camera offset or smth like that
            w_offset = 0.2 * w
            h_offset = 0.3 * h


            # Convert to camera pixels
            idx_x = int(index_tip.x * w)
            idx_y = int(index_tip.y * h)

            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            # Hand state logic
            handstate = HandTracker.fingers_state(hand_landmarks)

            if handstate != 0:
                # OPEN HAND → MOVE CURSOR

                # Scale camera coords to screen coords
                screen_x = np.interp(idx_x, (0 + w_offset, w - w_offset), (0, screen_w))
                screen_y = np.interp(idx_y, (0 + h_offset, h - h_offset), (0, screen_h))

                pyautogui.moveTo(screen_x, screen_y)

                if handstate == 2:
                    pyautogui.leftClick()


            # Debug visuals
            cv2.circle(img, (idx_x, idx_y), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (thumb_x, thumb_y), 15, (0, 255, 0), cv2.FILLED)

        # Show window
        cv2.imshow("Mouse and Keyboard Interface", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
