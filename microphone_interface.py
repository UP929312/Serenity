import time
import wave

import pyaudio

CHUNK_SIZE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Amount of bits per second
p = pyaudio.PyAudio()
ONE_SECONDS_WORTH = RATE

# https://people.csail.mit.edu/hubert/pyaudio/docs/#example-callback-mode-audio-i-o


class AudioRecordingHandler:
    """Handles the recording of audio from the microphone, compiling it as a single file/string of bytes (instead of frames)."""

    def __init__(self) -> None:
        self.stream: pyaudio.Stream | None = None

    def callback(self, in_data: bytes, frame_count: int, time_info: dict[str, float], status: int) -> tuple[bytes, int]:
        """Used as a callback for the pyaudio module, which runs this on it's own thread."""
        self.frames.append(in_data)
        # If len(data) is less than requested frame_count, PyAudio automatically assumes the stream is finished, and the stream stops.
        return (in_data, pyaudio.paContinue)  # This is required

    def start_recording(self) -> None:
        """Starts capturing audio data from the microphone and also starts a new thread to regularly save the audio data"""
        self.frames: list[bytes] = []  # Each frame should be a chunk of audio
        stream: pyaudio.Stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=self.callback,  # type: ignore[arg-type]
        )
        self.stream = stream

    def stop_recording(self, file_name: str) -> bytes:
        """Stops capturing audio data from the microphone and returns the audio bytes."""
        time.sleep(0.5)  # This is to make sure the chunks don't get truncated early
        assert self.stream is not None
        self.stream.stop_stream(); self.stream.close(); self.stream = None  # fmt: skip
        self.save_audio_file(self.frames, file_name)  # We save and load because for some reason this fixes things
        return self.load_audio_file(file_name)  # return b"".join(self.frames)  # This doesn't work for some reason

    @staticmethod
    def load_audio_file(file_name: str) -> bytes:
        """Loads an audio file from file and returns it as a byte string"""
        with open(file_name, "rb") as file:
            return file.read()

    @staticmethod
    def save_audio_file(audio_bytes: list[bytes], file_name: str) -> None:
        """Takes a byte string of the complete audio data and saves it as a .wav file"""
        with wave.open(file_name, "wb") as file:
            file.setnchannels(CHANNELS)
            file.setsampwidth(p.get_sample_size(FORMAT))
            file.setframerate(RATE)
            file.writeframes(b"".join(audio_bytes))


if __name__ == "__main__":

    from speech_to_text import STTHandler

    file_name = "assets/audio/recent_user_speech.wav"
    audio_handler = AudioRecordingHandler()

    print("About to start recording!")
    audio_handler.start_recording()
    time.sleep(5)
    print("Slept 5 seconds, stop recording!")
    audio_bytes = audio_handler.stop_recording(file_name)
    print("Done recording")

    print("Now transcribing")
    text = STTHandler(audio_bytes, time_transcription=True).transcribe()
    print(f"Stop recording function is returning: {text=}")
