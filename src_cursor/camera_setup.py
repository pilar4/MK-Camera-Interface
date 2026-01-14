import cv2
import pyautogui
import time

def camera_setup():
    screen_w, screen_h = pyautogui.size()
    print("screen width and height: ", screen_w, screen_h)

    for index in range(10):
        cap = cv2.VideoCapture(index)

        if cap.isOpened():
            # Try to read the first frame to see if it actually works
            ret, frame = cap.read()

            if ret:
                print(f"Displaying Camera Index [{index}] for 3 seconds...")

                # Start the timer
                start_time = time.time()

                # Loop for 3 seconds
                while (time.time() - start_time) < 1:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    cv2.imshow(f"Camera Index {index}", frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break


                cv2.destroyAllWindows()
                print(f" Camera Index [{index}] is WORKING")

            else:
                print(f" Camera Index [{index}] opens but returns no image (Black screen)")

        else:
            print(f" Camera Index [{index}] is empty")

        cap.release()

    print("--- Scan Complete ---")
    print("Which camera do you want to use?")
    camera_index = int(input())
    cap = cv2.VideoCapture(camera_index)

    camera_info = [cap, screen_w, screen_h]
    return camera_info