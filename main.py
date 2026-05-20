from system_control import set_volume, set_brightness
import cv2
from hand_tracker import HandTracker
from mouse_control import *

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

tracker = HandTracker()

cam_w = 1280
cam_h = 720

cap.set(3, cam_w)
cap.set(4, cam_h)

dragging = False
pinch_active = False
click_cooldown = 0

while True:

    success, img = cap.read()

    if not success:
        continue

    img, lm = tracker.find_hands(img)

    if lm:

        fingers = tracker.fingers_up(lm)

        # -----------------
        # CURSOR MOVEMENT
        # -----------------

        x = lm[8][1]
        y = lm[8][2]

        # move only when NOT dragging
        if not dragging:
            move_mouse(x, y, cam_w, cam_h)


        # -----------------
        # PINCH FOR DRAG
        # -----------------

        dist = tracker.find_distance(4, 8, lm)

        if dist < 40:

            pinch_active = True

            if not dragging:
                drag()
                dragging = True

        else:

            pinch_active = False

            if dragging:
                release()
                dragging = False


        # -----------------
        # DOUBLE CLICK (2 fingers)
        # -----------------

        if fingers == [0,1,1,0,0] and click_cooldown == 0:
            click()
            click()   # double click
            click_cooldown = 10


        # cooldown
        if click_cooldown > 0:
            click_cooldown -= 1


        # -----------------
        # SCROLL
        # -----------------

        if fingers == [0,1,1,1,0]:
            scroll_up()

        if fingers == [0,1,1,1,1]:
            scroll_down()


        # -----------------
        # VOLUME CONTROL (thumb + index)
        # -----------------

        dist_vol = tracker.find_distance(4, 8, lm)

        if fingers == [1, 1, 0, 0, 0]:
            set_volume(dist_vol)


        # -----------------
        # BRIGHTNESS CONTROL (thumb + middle)
        # -----------------

        dist_bright = tracker.find_distance(4, 12, lm)

        if fingers == [1, 0, 1, 0, 0]:
            set_brightness(dist_bright)


        # -----------------
        # DEBUG DISPLAY
        # -----------------

        cv2.putText(
            img,
            str(fingers),
            (20,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )


    cv2.imshow("GestureOS", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()