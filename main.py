from datetime import datetime

from agent_avatar import AgentAvatar
from ai_interface import AgentInterface
from conversation_store import store_conversation_row
from detect_facial_expression import get_facial_emotion, test_camera_accessible
from keyboard_detection import KeyboardDetection
from pyaudio_interface import start_recording, stop_recording
from sentiment_analysis import detect_sentiment
from speech_to_text import convert_speech_to_text
from text_to_speech import convert_text_to_speech

import cv2
from pyaudio import Stream

username = "test_user"
WINDOW_NAME = "Serenity"

active = cv2.imread("being_pressed.png")
inactive = cv2.imread("not_being_pressed.png")

class Handler:
    def __init__(self, username: str) -> None:
        self.username = username
        self.stream: Stream = None
        cv2.imshow(WINDOW_NAME, inactive)
        self.keyboard_detection = KeyboardDetection("b", self.on_press_speak_key, self.on_release_speak_key)
        self.agent = AgentInterface()
        self.agent_avatar = AgentAvatar()

        self.last_agent_response = ""
        self.last_human_response = ""
        self.last_agent_response_sentiment = "neutral"

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
        #emotion = get_facial_emotion()  # Currently Unused
        speech_segment = stop_recording(self.stream)
        user_input = convert_speech_to_text(speech_segment)
        user_sentiment = detect_sentiment(user_input)
        store_conversation_row(self.username, user_input, "user", user_sentiment)

        agent_output = self.agent.continue_chain(human_input=user_input)
        self.last_agent_response_sentiment = detect_sentiment(agent_output)
        store_conversation_row(self.username, agent_output, "agent", self.last_agent_response_sentiment)

        convert_text_to_speech(agent_output, play_message=True)
        #print(output)

    def main_loop(self) -> None:
        while True:
            #print("Main loop")
            # Handle keypresses
            #self.keyboard_detection.handle_thread()
            # Handle agent avatar
            self.agent_avatar.animate(self.last_agent_response_sentiment)

if test_camera_accessible():
    cv2.namedWindow(WINDOW_NAME)
    handler = Handler(username).main_loop()
else:
    cv2.imshow("Camera not accessible", cv2.imread("camera_not_accessible.png"))
    cv2.waitKey(0)