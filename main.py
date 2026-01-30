import cv2
from src_cursor import camera_setup
from src_cursor.cursor import Cursor
from src_cursor.hand_tracker import HandTracker
import threading
from queue import Queue
# from speech_to_text import speech_worker, typeKey


def main():

    camera_info = camera_setup.camera_setup()
    cap = camera_info[0]
    screen_w = camera_info[1]
    screen_h = camera_info[2]

    if cap is None:
        return

    tracker = HandTracker()

    cursor = Cursor(screen_w, screen_h)

    # text_queue = Queue()
    # stop_event = threading.Event()

    # speech_thread = threading.Thread(
    #     target=speech_worker,
    #     args=(text_queue, stop_event),
    #     daemon=True
    # )
    # speech_thread.start()


    print("System Ready. Press 'q' to quit.")

    while True:
        # --- speech input ---
        # while not text_queue.empty():
        #     text = text_queue.get()
        #
        #     if text in ("exit", "quit", "stop"):
        #         stop_event.set()
        #         break
        #
        #     typeKey(text)



        # --- camera input --
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        results = tracker.scan_hands(img)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            wrist_point = hand_landmarks.landmark[0] # <---- decided to change tracking from index to wrist
            thumb_tip = hand_landmarks.landmark[4]   # it reduced cursor jumping when clicking to almost 0 jump

            wrist_x = int(wrist_point.x * w)
            wrist_y = int(wrist_point.y * h)

            thumb_x = int(thumb_tip.x * w)
            thumb_y = int(thumb_tip.y * h)


            handstate = HandTracker.fingers_state(hand_landmarks)


            cursor.move_and_click(wrist_x, wrist_y, handstate, w, h)

        cv2.imshow("Mouse and Keyboard Interface", img)

        # if stop_event.is_set() or cv2.waitKey(1) & 0xFF == ord('q'):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
