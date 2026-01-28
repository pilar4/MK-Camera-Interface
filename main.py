import cv2
from src_cursor import camera_setup
from src_cursor.cursor import Cursor
from src_cursor.hand_tracker import HandTracker


def main():

    camera_info = camera_setup.camera_setup()
    cap = camera_info[0]
    screen_w = camera_info[1]
    screen_h = camera_info[2]

    if cap is None:
        return

    tracker = HandTracker()

    cursor = Cursor(screen_w, screen_h)


    print("System Ready. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        results = tracker.scan_hands(img)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]

            idx_x = int(index_tip.x * w)
            idx_y = int(index_tip.y * h)

            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)


            handstate = HandTracker.fingers_state(hand_landmarks)


            cursor.move_and_click(idx_x, idx_y, handstate, w, h)

        cv2.imshow("Mouse and Keyboard Interface", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()