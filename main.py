from agent_avatar import AgentAvatar
from ai_interface import AgentInterface
from conversation_store import store_conversation_row
from keyboard_detection import KeyboardDetection
from polly import convert_text_to_speech
from pyaudio_interface import start_recording, stop_recording
from speech_to_text import convert_speech_to_text

import cv2
from pyaudio import Stream

WINDOW_NAME = "Serenity"

active = cv2.imread("being_pressed.png")
inactive = cv2.imread("not_being_pressed.png")
cv2.namedWindow(WINDOW_NAME)

class Handler:
    def __init__(self) -> None:
        self.stream: Stream = None
        cv2.imshow(WINDOW_NAME, inactive)
        self.keyboard_detection = KeyboardDetection("b", self.on_press_speak_key, self.on_release_speak_key)
        self.agent = AgentInterface()
        self.agent_avatar = AgentAvatar()

    def on_press_speak_key(self) -> None:
        ''' Start recording mic data'''
        print("Key pressed")
        cv2.imshow(WINDOW_NAME, active)
        self.stream = start_recording()

    def on_release_speak_key(self) -> None:
        ''' Stop recording mic data '''
        cv2.imshow(WINDOW_NAME, inactive)
        print("Key released")
        return
        speech_segment = stop_recording(self.stream)
        text = convert_speech_to_text(speech_segment)
        store_conversation_row(text, "user", None)

        output = self.agent.continue_chain(human_input=text)
        store_conversation_row(text, "agent", None)

        convert_text_to_speech(output, play_message=True)
        #print(output)


    def main_loop(self) -> None:
        while True:
            #print("Main loop")
            self.keyboard_detection.handle_thread()
            #print("Next")
            
handler = Handler().main_loop()