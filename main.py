
from typing import TYPE_CHECKING

from agent_avatar import AgentAvatar
from ai_interface import AgentInterface
from conversation_store import store_conversation_row
from detect_facial_expression import test_camera_accessible  # , get_facial_emotion
from keyboard_detection import KeyboardDetection
from pyaudio_interface import AudioRecordingHandler
from sentiment_analysis import detect_sentiment
from text_to_speech import convert_text_to_speech

import cv2  # type: ignore[import]

if TYPE_CHECKING:
    from pyaudio import Stream

username = "test_user"
WINDOW_NAME = "Serenity"
BYPASS_CAMERA_CHECK = True

active = cv2.imread("assets/images/being_pressed.png")
inactive = cv2.imread("assets/images/not_being_pressed.png")


class MainLoopHandler:
    def __init__(self, username: str) -> None:
        cv2.imshow(WINDOW_NAME, inactive)

        self.username = username
        self.stream: Stream | None = None
        self.keyboard_detection = KeyboardDetection(" ", self.on_press_speak_key, self.on_release_speak_key)
        self.agent = AgentInterface()
        self.agent_avatar = AgentAvatar()
        self.current_monolog_text = ""
        self.audio_handler = AudioRecordingHandler()  # type: ignore

        self.last_agent_response_sentiment = "neutral"

    def main_loop(self) -> None:
        """
        The main program loop, polls the keyboard for key presses, \n
        and when it detects the right one, will fire `on_press_speak_key()`
        """
        while True:
            print("Loopady doop")
            self.keyboard_detection.detect_key_press()

    def on_press_speak_key(self) -> None:
        """ Calls the audio handler to start recording mic data. """
        print("Key pressed")
        cv2.imshow(WINDOW_NAME, active)
        self.audio_handler.start_recording()

    def on_release_speak_key(self) -> None:
        """Stop recording mic data"""
        cv2.imshow(WINDOW_NAME, inactive)
        print("Key released")
        # emotion = get_facial_emotion()  # Currently Unused
        user_input = self.audio_handler.stop_recording()
        print(f"{user_input=}")
        if user_input == "":
            print("Nothing, so returning")
            return
        print("Returning anyway")
        return
        # user_input = "Hello there"
        user_sentiment, confidence = detect_sentiment(user_input)
        # store_conversation_row(
        #    self.username, user_input, "user", user_sentiment if confidence > 0.1 else None, facial_emotion=None
        # )  # fmt: ignore

        agent_output = self.agent.continue_chain(human_input=user_input)
        # self.last_agent_response_sentiment = detect_sentiment(agent_output)[0]
        # store_conversation_row(
        #    self.username, agent_output, "agent", self.last_agent_response_sentiment, facial_emotion=None
        # )  # fmt: ignore

        convert_text_to_speech(agent_output, play_message=True)


if BYPASS_CAMERA_CHECK or test_camera_accessible():
    cv2.namedWindow(WINDOW_NAME)
    handler = MainLoopHandler(username)
    handler.main_loop()
else:
    cv2.imshow("Camera not accessible", cv2.imread("assets/images/camera_not_accessible.png"))
    cv2.waitKey(0)
