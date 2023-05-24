from typing import Any, Callable

import cv2  # type: ignore[import]

WINDOW_NAME = "Serenity"


class KeyboardDetection:
    """A class which will be regularly polled to check if the correct key was pressed, and if so, will call the appropriate function."""

    def __init__(self, key_to_press: str, on_key_press: Callable[..., Any], on_key_release: Callable[..., Any]) -> None:
        self.key_to_press = key_to_press
        self.key_pressed = False
        self.on_key_press = on_key_press
        self.on_key_release = on_key_release

        self.down_barrier = True

    def detect_key_press(self) -> None:
        """
        Detects if the selected key was pressed, and if so, calls the appropriate function.\n
        This function also filters out a bug with the library where it detects the keystroke twice, hence the gate.
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
            if self.down_barrier:  # If the initial stop is active, disable it, then the next case will pass
                self.down_barrier = False
                return
            self.on_key_press()
            self.key_pressed = True
            self.down_barrier = True


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
    keyboard_detection = KeyboardDetection(" ", on_key_press, on_key_release)
    while True:
        keyboard_detection.detect_key_press()
