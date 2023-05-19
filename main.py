from datetime import datetime
from typing import TYPE_CHECKING

from agent_avatar import AgentAvatar
from ai_interface import AgentInterface
from conversation_store import store_conversation_row
from detect_facial_expression import get_facial_emotion, test_camera_accessible
from keyboard_detection import KeyboardDetection
from pyaudio_interface import AudioRecordingHandler
from sentiment_analysis import detect_sentiment
from speech_to_text import convert_speech_to_text
from text_to_speech import convert_text_to_speech

import cv2  # type: ignore[import]

if TYPE_CHECKING:
    from pyaudio import Stream

username = "test_user"
WINDOW_NAME = "Serenity"

active = cv2.imread("being_pressed.png")
inactive = cv2.imread("not_being_pressed.png")


class Handler:
    def __init__(self, username: str) -> None:
        cv2.imshow(WINDOW_NAME, inactive)

        self.username = username
        self.stream: Stream | None = None
        self.keyboard_detection = KeyboardDetection("b", self.on_press_speak_key, self.on_release_speak_key)
        self.agent = AgentInterface()
        self.agent_avatar = AgentAvatar()
        self.audio_handler = AudioRecordingHandler()

        self.last_agent_response_sentiment = "neutral"

    def on_press_speak_key(self) -> None:
        """Start recording mic data"""
        print("Key pressed")
        cv2.imshow(WINDOW_NAME, active)
        self.audio_handler.start_recording()

    def on_release_speak_key(self) -> None:
        """Stop recording mic data"""
        cv2.imshow(WINDOW_NAME, inactive)
        print("Key released")
        # return
        # emotion = get_facial_emotion()  # Currently Unused
        assert self.stream is not None
        speech_segment = self.audio_handler.stop_recording()
        # user_input = convert_speech_to_text(speech_segment)
        user_input = "Hello there"
        user_sentiment, confidence = detect_sentiment(user_input)
        store_conversation_row(
            self.username, user_input, "user", datetime.now(), user_sentiment if confidence > 0.1 else None, facial_emotion=None
        )  # fmt: ignore

        agent_output = self.agent.continue_chain(human_input=user_input)
        self.last_agent_response_sentiment = detect_sentiment(agent_output)[0]
        store_conversation_row(
            self.username, agent_output, "agent", datetime.now(), self.last_agent_response_sentiment, facial_emotion=None
        )  # fmt: ignore

        convert_text_to_speech(agent_output, play_message=True)
        # print(output)

    def main_loop(self) -> None:
        while True:
            # print("Main loop")
            # Handle keypresses
            # self.keyboard_detection.handle_thread()
            self.keyboard_detection.detect_key_press()
            # Handle agent avatar
            self.agent_avatar.animate(self.last_agent_response_sentiment)  # Should be threaded, but currently does nothing


if test_camera_accessible():
    cv2.namedWindow(WINDOW_NAME)
    handler = Handler(username)
    handler.main_loop()
else:
    cv2.imshow("Camera not accessible", cv2.imread("camera_not_accessible.png"))
    cv2.waitKey(0)
