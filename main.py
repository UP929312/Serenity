from polly import convert_text_to_speech
from speech_to_text import send_receive
from keyboard_detection import KeyboardDetection

import cv2

from pyaudio_interface import stream#, FRAMES_PER_BUFFER
#import asyncio

WINDOW_NAME = "img"

active = cv2.imread("being_pressed.png")
inactive = cv2.imread("not_being_pressed.png")

cv2.namedWindow(WINDOW_NAME)

class Handler:
    def __init__(self) -> None:
        self.stream = stream
        cv2.imshow(WINDOW_NAME, inactive)
        self.keyboard_detection = KeyboardDetection("b", self.on_press_speak_key, self.on_release_speak_key)

    def on_press_speak_key(self) -> None:
        print("Key pressed")
        cv2.imshow(WINDOW_NAME, active)
        #asyncio.run(send_receive())

    def on_release_speak_key(self) -> None:
        cv2.imshow(WINDOW_NAME, inactive)
        print("Key released")

    def main_loop(self) -> None:
        while True:
            #print("Main loop")
            self.keyboard_detection.handle_thread()
            #print("Next")
            
handler = Handler().main_loop()