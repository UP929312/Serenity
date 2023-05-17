from threading import Thread
from typing import Callable, Any
import cv2  # type: ignore[import]

WINDOW_NAME = "Serenity"


class KeyboardDetection:
    def __init__(self, 
                 key_to_press: str, 
                 on_key_press: Callable[..., Any], 
                 on_key_release: Callable[..., Any]
        ) -> None:
        self.key_to_press = key_to_press
        self.key_pressed = False
        self.on_key_press = on_key_press
        self.on_key_release = on_key_release

        self.thread_exists = False

        self.down_barrier = 0
        self.up_barrier = 0

    def handle_thread(self) -> None:
        if not self.thread_exists:
            thread = Thread(target=self.detect_key_press)
            thread.start()

    def detect_key_press(self) -> None:
        self.thread_exists = True
        print("Thread started")
        while True:
            print("loop")
            k = cv2.waitKey(33)
            # print(k)
            if k == -1:  # No key pressed
                # print("Nothing")
                if self.key_pressed:
                    if self.up_barrier:  # If the initial stop is active, disable it, then the next case will pass
                        self.up_barrier -= 1
                        continue
                    # print("A stopped being pressed")
                    self.key_pressed = False
                    self.on_key_release()
            else:
                # print("Key pressed!", k)
                if chr(k) != self.key_to_press:  # If it's not the key we want
                    continue
                if self.key_pressed:  # If it's already pressed
                    continue
                if self.down_barrier > 0:  # If the initial stop is active, disable it, then the next case will pass
                    self.down_barrier -= 1
                    continue
                self.key_pressed = True
                self.up_barrier = 10
                self.down_barrier = 10
                # print("A started being pressed")


def on_key_press() -> None:
    print("Key pressed")


def on_key_release() -> None:
    print("Key released")


if __name__ == "__main__":
    img = cv2.imread("not_being_pressed.png")
    cv2.imshow(WINDOW_NAME, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    keyboard_detection = KeyboardDetection("b", on_key_press, on_key_release)
    keyboard_detection.handle_thread()
