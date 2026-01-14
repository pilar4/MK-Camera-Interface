import cv2
from src_cursor import camera_setup
from src_cursor.cursor import Cursor
from src_cursor.hand_tracker import HandTracker


def main():
    """SETUP"""
    # 1. Camera Setup
    camera_info = camera_setup.camera_setup()
    cap = camera_info[0]
    screen_w = camera_info[1]
    screen_h = camera_info[2]

    if cap is None:
        return

    # 2. Tracker
    tracker = HandTracker()

    # 3. Cursor
    cursor = Cursor(screen_w, screen_h)


    print("System Ready. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            break

        # Mirror image for natural interaction
        img = cv2.flip(img, 1)
        h, w, _ = img.shape  # Get image dimensions

        # Scan hands
        results = tracker.scan_hands(img)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Get necessary landmarks
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            # Convert normalized coordinates (0.0 - 1.0) to pixels
            idx_x = int(index_tip.x * w)
            idx_y = int(index_tip.y * h)

            # (Optional) Thumb coords for drawing
            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)

            # Get Hand State (0=Idle, 1=Move, 2=Click)
            handstate = HandTracker.fingers_state(hand_landmarks)

            # --- DELEGATE TO CURSOR CLASS ---
            # We pass the raw data; the class handles mapping and clicking
            cursor.move_and_click(idx_x, idx_y, handstate, w, h)

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