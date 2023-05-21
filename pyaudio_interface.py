import asyncio
import time
import pyaudio
import threading
import wave
from datetime import datetime

from speech_to_text import STTWebhookHandler

CHUNK_SIZE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Amount of bits per second
p = pyaudio.PyAudio()
ONE_SECONDS_WORTH = RATE


class AudioRecordingHandler:
    """
    A class that handles the recording of audio from the microphone, compiling it as a single file (instead of frames).\n
    It also sends the audio data to the Speech to Text API (AssemblyAI) and receives text data back.
    """

    def __init__(self) -> None:
        self.stream: pyaudio.Stream | None = None
        self.frames: list[bytes] = []  # Each frame should be 1 second of audio
        self.speech_to_text_wh_handler = STTWebhookHandler(self.on_receive)
        self.current_monolog_text = ""

    def on_receive(self, text: str) -> None:
        """Runs when the STTWebhookHandler receives a new text from the API."""
        self.current_monolog_text = text

    def save_one_second(self) -> None:
        """
        Runs in another thread and regularly polls the audio stream in from the microphone, \n
        appends it to it's list, and sends it to the speech to text API.
        """
        while True:
            if self.stream is None:
                return
            start_time = datetime.now()
            try:
                frame = self.stream.read(ONE_SECONDS_WORTH)
                self.frames.append(frame)
            except OSError:  # OSError: [Errno -9981] Input overflowed
                return

            end_time = datetime.now()
            time_taken = (end_time - start_time).total_seconds()
            if time_taken < 1:
                time.sleep(1 - time_taken)
            self.speech_to_text_wh_handler.send(frame)

    def start_recording(self) -> None:
        """Starts capturing audio data from the microphone and also starts a new thread to regularly save the audio data"""
        stream: pyaudio._Stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )
        self.stream = stream

        thread = threading.Thread(target=self.save_one_second)
        thread.start()

    def stop_recording(self, file_name: str | None = None) -> str:
        """Stops capturing audio data from the microphone and returns the complete audio transcript as a string."""
        time.sleep(0.5)  # This is to make sure the chunks don't get truncated early
        assert self.stream is not None
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        time.sleep(0.5)  # To wait for the remaining webhooks to come in
        complete_recording = b"".join(self.frames)
        if file_name:
            self.save_audio_file(complete_recording, file_name)
        print(f"{self.current_monolog_text=}")
        return self.current_monolog_text

    def save_audio_file(self, complete_recording: bytes, file_name: str) -> None:
        """Takes a byte string of the complete audio data and saves it as a .wav file"""
        print("Saving audio file as", file_name)
        sample_size = p.get_sample_size(FORMAT)

        with wave.open(file_name, "wb") as file:
            file.setnchannels(CHANNELS)
            file.setsampwidth(sample_size)
            file.setframerate(RATE)
            file.writeframes(complete_recording)
        print("Post saving file (won't happen normally))")


if __name__ == "__main__":
    audio_handler = AudioRecordingHandler()
    print("Start recording!")
    audio_handler.start_recording()
    time.sleep(5)
    print("Slept 5 seconds")
    print("Stop recording!")
    audio_handler.stop_recording("assets/audio/test.wav")
    print(audio_handler.current_monolog_text)
