from typing import TYPE_CHECKING

from elevenlabs import play

from agent_avatar import AgentAvatar
from ai_interface import AgentInterface

# from conversation_store import store_conversation_row
# from detect_facial_expression import get_facial_emotion
from keyboard_detection import KeyboardDetection
from microphone_interface import AudioRecordingHandler
from sentiment_analysis import detect_sentiment
from speech_to_text import STTHandler

# from text_optimiser import TextOptimiser
from text_to_speech import convert_text_to_speech

from cv2_utils import show_image, show_text, test_camera_accessible

if TYPE_CHECKING:
    from pyaudio import Stream

WINDOW_NAME = "Serenity"
BYPASS_CAMERA_CHECK = True


class MainLoopHandler:
    def __init__(self, username: str) -> None:
        self.username = username
        self.stream: Stream | None = None
        self.keyboard_detection = KeyboardDetection(" ", self.on_press_speak_key, self.on_release_speak_key)
        self.agent = AgentInterface()
        self.agent_avatar = AgentAvatar()
        self.audio_handler = AudioRecordingHandler()

        self.current_monolog_text = ""
        self.last_agent_response_sentiment = "neutral"

    def main_loop(self) -> None:
        """
        The main program loop, polls the keyboard for key presses, \n
        and when it detects the right one, will fire `on_press_speak_key()`
        """
        show_image("inactive")
        with open("assets/audio/introduction_script.mp3", "rb") as f:
            play(f.read())

        while True:
            # print("Loopady doop")
            self.keyboard_detection.detect_key_press()

    def on_press_speak_key(self) -> None:
        """Calls the audio handler to start recording mic data."""

        show_image("active")
        self.audio_handler.start_recording()

    def on_release_speak_key(self) -> None:
        """Stop recording mic data"""
        show_image("inactive")
        # emotion = get_facial_emotion()  # Currently Unused
        user_input_audio_bytes = self.audio_handler.stop_recording("assets/audio/most_recent_user_speech.wav")
        user_input_text = STTHandler(user_input_audio_bytes, False).transcribe()
        # show_text("inactive", user_input_text, position=(10, 500), color=(255, 255, 255))
        print(f"{user_input_text=}")

        if user_input_text == "":
            with open("assets/audio/no_input_script.mp3", "rb") as f:
                play(f.read())
            return
        user_sentiment, confidence = detect_sentiment(user_input_text)
        print(f"{user_sentiment=} {confidence=}")
        # store_conversation_row(
        #    self.username, user_input, "user", user_sentiment if confidence > 0.1 else None, facial_emotion=None
        # )  # fmt: ignore

        # When the AI is called, it will have the following data:
        # Human's text, Human's facial expression (Sad, Happy, etc), Human's text's sentiment (Positive, Negative, Neutral)
        agent_output = self.agent.continue_chain(human_input=user_input_text)
        # self.last_agent_response_sentiment = detect_sentiment(agent_output)[0]
        # store_conversation_row(
        #    self.username, agent_output, "agent", self.last_agent_response_sentiment, facial_emotion=None
        # )  # fmt: ignore

        # optimised_text = TextOptimiser(agent_output, False).optimised_text
        optimised_text = agent_output
        print(f"{optimised_text=}")
        convert_text_to_speech(optimised_text, voice_type="young-female-british", play_message=True)


if BYPASS_CAMERA_CHECK or test_camera_accessible():
    handler = MainLoopHandler(username="test_user")
    handler.main_loop()
else:
    show_image("assets/images/camera_not_accessible.png", wait_for_key_press=True)
