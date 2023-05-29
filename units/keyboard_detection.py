from typing import Callable

import cv2  # type: ignore[import]
from cv2_utils import show_image

WINDOW_NAME = "Serenity"


class KeyboardDetection:
    """A class which will be regularly polled to check if the correct key was pressed, and if so, will call the appropriate function."""

    def __init__(self, key_to_press: str, on_key_press: Callable[[], None], on_key_release: Callable[[], None]) -> None:
        self.key_to_press = key_to_press
        self.key_pressed = False
        self.on_key_press = on_key_press
        self.on_key_release = on_key_release

        self.down_barrier = True

    def detect_key_press(self) -> None:
        """
        Detects if the selected key was pressed, and if so, calls the appropriate function.\n
        This function also filters out a bug with the library where it detects the keystroke twice, hence the gate/barrier.
        """
        k = cv2.waitKey(32)  # 32 is the minimum/maximum delay
        # print(k)
        if k == -1 or chr(k) != self.key_to_press:  # No key pressed
            if self.key_pressed:
                self.key_pressed = False
                self.on_key_release()
        else:
            # print("Key pressed!", self.key_to_press)
            if self.key_pressed or chr(k) != self.key_to_press:  # If it's already pressed, or a different key
                return
            if self.down_barrier:  # If the initial stop is active, disable it, then the next case will pass (prevents double presses)
                self.down_barrier = False
                return
            self.on_key_press()
            self.key_pressed, self.down_barrier = True, True


if __name__ == "__main__":

    def on_key_press() -> None:
        show_image("active")
        print("Key pressed")

    def on_key_release() -> None:
        show_image("inactive")
        print("Key released")

    show_image("inactive")
    keyboard_detection = KeyboardDetection(" ", on_key_press, on_key_release)
    while True:
        keyboard_detection.detect_key_press()
