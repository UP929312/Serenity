from datetime import datetime, timedelta

from elevenlabs import play

from cv2_utils import show_image, show_text, test_camera_accessible
from microphone_interface import AudioRecordingHandler
from units.agent_avatar import AgentAvatar
from units.ai_interface import AgentInterface

# from units.vector_database import store_conversation_row
# from units.detect_facial_expression import get_facial_emotion
from units.keyboard_detection import KeyboardDetection
from units.sentiment_analysis import detect_sentiment
from units.speech_to_text import STTHandler
from units.text_optimiser import TextOptimiser
from units.text_to_speech import convert_text_to_speech

BYPASS_CAMERA_CHECK = True
SKIP_INTRO = True


class MainLoopHandler:
    def __init__(self, username: str) -> None:
        self.username = username
        self.keyboard_detection = KeyboardDetection(" ", self.on_press_speak_key, self.on_release_speak_key)
        self.agent = AgentInterface()
        self.agent_avatar = AgentAvatar()
        self.audio_handler = AudioRecordingHandler()
        self.session_start_time = datetime.now()

    def main_loop(self) -> None:
        """
        The main program loop, polls the keyboard for key presses, \n
        and when it detects the right one, will fire `on_press_speak_key()`
        """
        show_image("inactive")
        if not SKIP_INTRO:
            with open("assets/audio/introduction_script.mp3", "rb") as f:
                play(f.read())

        while True:
            # print("Loopady doop")
            self.keyboard_detection.detect_key_press()

    def on_press_speak_key(self) -> None:
        """Calls the audio handler to start recording mic data."""
        print("Key pressed", end="    ")
        show_image("active")
        self.audio_handler.start_recording()

    def on_release_speak_key(self) -> None:
        """Stop recording mic data, and calls the main processing function"""
        print("Key released")
        show_image("inactive")
        # emotion = get_facial_emotion()  # Currently Unused
        user_input_audio_bytes = self.audio_handler.stop_recording("assets/audio/most_recent_user_speech.wav")
        self.new_human_input(user_input_audio_bytes)

    def new_human_input(self, user_input_audio_bytes: bytes) -> None:
        """Takes a segment of human speech, and processes it."""
        user_input_text, _ = STTHandler(user_input_audio_bytes, False).transcribe()
        # show_text("inactive", user_input_text, position=(10, 500), color=(255, 255, 255))
        print(f"{user_input_text=}", end=" ")

        if user_input_text == "":
            with open("assets/audio/no_input_script.mp3", "rb") as f:
                play(f.read())
            return

        #user_sentiment, confidence = detect_sentiment(user_input_text)
        #print(f"User's sentiment: {user_sentiment}, confidence: {confidence}")
        # store_conversation_row(self.username, user_input, "user", user_sentiment if confidence > 0.1 else None, facial_emotion=None)  # fmt: ignore

        # When the AI is called, it will have the following data:
        # Human's text, Human's facial expression (Sad, Happy, etc), Human's text's sentiment (Positive, Negative, Neutral)
        agent_output = self.agent.continue_chain(human_input=user_input_text)
        # last_agent_response_sentiment = detect_sentiment(agent_output)[0]
        # store_conversation_row(self.username, agent_output, "agent", last_agent_response_sentiment, facial_emotion=None)  # fmt: ignore

        optimised_text = TextOptimiser(agent_output, print_improvement=False, disabled=True).optimised_text
        # print(f"{optimised_text=}")
        convert_text_to_speech(optimised_text, voice_type="young-female-british", play_message=True)

        # If it's been an hour
        if datetime.now() > self.session_start_time + timedelta(hours=1):
            print("It's been an hour!")


if BYPASS_CAMERA_CHECK or test_camera_accessible():
    handler = MainLoopHandler(username="test_user")
    handler.main_loop()
else:
    show_image("assets/images/camera_not_accessible.png", wait_for_key_press=True)
