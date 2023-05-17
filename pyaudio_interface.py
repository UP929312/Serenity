from datetime import datetime
import pyaudio
import wave

CHUNK_SIZE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Maybe up it to 44100? 16000 is the minimum that sounds 'okay'
p = pyaudio.PyAudio()


def save_audio_file(data: bytes, duration_in_seconds: int, file_name: str) -> None:
    sample_size = p.get_sample_size(FORMAT)
    frames = []  # Initialize array to store frames
    for _ in range(0, int(RATE / CHUNK_SIZE * duration_in_seconds)):
        print("frame generated")
        data = stream.read(CHUNK_SIZE)  # This is super slowwww
        frames.append(data)
    
    with wave.open(file_name, 'wb') as file:
        file.setnchannels(CHANNELS)
        file.setsampwidth(sample_size)
        file.setframerate(RATE)
        file.writeframes(b''.join(frames))


def start_recording() -> tuple[pyaudio.Stream, datetime]:
    stream: pyaudio._Stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )
    return stream, datetime.now()


def stop_recording(stream: pyaudio.Stream, start_datetime: datetime, file_name: str | None = None) -> bytes:
    duration_in_seconds = int((datetime.now() - start_datetime).total_seconds())
    data = stream.read(CHUNK_SIZE)
    if file_name:
        save_audio_file(data, duration_in_seconds, file_name)
    stream.stop_stream()
    stream.close()
    return data

if __name__ == "__main__":
    import time
    print("Starting recording")
    stream, start_datetime = start_recording()
    time.sleep(3)
    print("Finished recording")
    stop_recording(stream, start_datetime, "audio_recording.mp3")