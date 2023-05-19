import pyaudio
import wave
import threading
import time
import asyncio
from datetime import datetime
from typing import Callable

CHUNK_SIZE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Amount of bits per second
p = pyaudio.PyAudio()
ONE_SECONDS_WORTH = RATE


class AudioRecordingHandler:
    def __init__(self, on_save_audio: Callable[[bytes], None]) -> None:
        self.stream: pyaudio.Stream | None = None
        self.frames: list[bytes] = []  # Each frame should be 1 second of audio
        self.on_save_audio = on_save_audio

    def save_one_second(self) -> None:
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
            # event_loop = asyncio.get_event_loop()
            # event_loop.run_until_complete(on_save_audio(frame))

    def start_recording(self) -> None:
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

    def stop_recording(self, file_name: str | None = None) -> bytes:
        time.sleep(0.5)  # This is to make sure the chunks don't get truncated
        assert self.stream is not None
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        complete_recording = b"".join(self.frames)
        if file_name:
            self.save_audio_file(complete_recording, file_name)
        return complete_recording

    def save_audio_file(self, complete_recording: bytes, file_name: str) -> None:
        print("Saving audio file as ", file_name)
        sample_size = p.get_sample_size(FORMAT)

        with wave.open(file_name, "wb") as file:
            file.setnchannels(CHANNELS)
            file.setsampwidth(sample_size)
            file.setframerate(RATE)
            file.writeframes(complete_recording)
        print("Post saving file (won't happen normally))")


def on_save_audio(frame: bytes) -> None:
    pass


if __name__ == "__main__":
    audio_handler = AudioRecordingHandler(on_save_audio)
    print("Start recording!")
    audio_handler.start_recording()
    time.sleep(5)
    print("Slept 5 seconds")
    print("Stop recording!")
    audio_handler.stop_recording("assets/audio/test.wav")
