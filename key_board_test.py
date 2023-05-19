import cv2  # type: ignore[import]

img = cv2.imread("not_being_pressed.png")  # load a dummy image
being_pressed = False
key_to_press = "a"

THRESHOLD = 10

down_barrier = 0
up_barrier = 0
while True:
    cv2.imshow("img", img)
    k = cv2.waitKey(33)
    if k == 27:  # Esc key to stop
        break
    elif k == -1:  # normally -1 returned,so don't print it
        if being_pressed:
            if up_barrier:  # If the initial stop is active, disable it, then the next case will pass
                up_barrier -= 1
                continue
            print("A stopped being pressed")
            being_pressed = False
            img = cv2.imread("not_being_pressed.png")

    else:
        if chr(k) == key_to_press:
            if not being_pressed:
                if down_barrier > 0:
                    down_barrier -= 1
                    continue
                being_pressed = True
                img = cv2.imread("being_pressed.png")
                up_barrier = 10
                down_barrier = 10
                print("A started being pressed")
