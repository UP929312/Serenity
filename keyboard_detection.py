# from threading import Thread
from typing import Callable, Any
import cv2  # type: ignore[import]

WINDOW_NAME = "Serenity"


class KeyboardDetection:
    def __init__(self, key_to_press: str, on_key_press: Callable[..., Any], on_key_release: Callable[..., Any]) -> None:
        self.key_to_press = key_to_press
        self.key_pressed = False
        self.on_key_press = on_key_press
        self.on_key_release = on_key_release

        self.down_barrier = 1

    def detect_key_press(self) -> None:
        for _ in range(1):  # TODO: Remove this kind of stuff
            k = cv2.waitKey(32)  # 32 is the minimum/maximum delay
            # print(k)
            if k == -1 and chr(k) != self.key_to_press:  # No key pressed
                if self.key_pressed:
                    self.key_pressed = False
                    self.on_key_release()
            else:
                # print("Key pressed!", self.key_to_press)
                if chr(k) != self.key_to_press:  # If it's not the key we want
                    continue
                if self.key_pressed:  # If it's already pressed
                    continue
                # print(self.down_barrier)
                if self.down_barrier > 0:  # If the initial stop is active, disable it, then the next case will pass
                    self.down_barrier -= 1
                    continue
                self.on_key_press()
                self.key_pressed = True
                self.down_barrier = 1
                # print("A started being pressed")


if __name__ == "__main__":

    def on_key_press() -> None:
        cv2.imshow(WINDOW_NAME, active)
        print("Key pressed")

    def on_key_release() -> None:
        cv2.imshow(WINDOW_NAME, inactive)
        print("Key released")

    active = cv2.imread("assets/images/being_pressed.png")
    inactive = cv2.imread("assets/images/not_being_pressed.png")
    cv2.imshow(WINDOW_NAME, inactive)
    keyboard_detection = KeyboardDetection("b", on_key_press, on_key_release)
    while True:
        keyboard_detection.detect_key_press()
