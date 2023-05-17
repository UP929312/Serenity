import pyaudio
import wave

CHUNK_SIZE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Maybe up it to 44100?
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

def start_recording() -> pyaudio.Stream:
    stream: pyaudio._Stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )
    return stream


def stop_recording(stream: pyaudio.Stream, duration_in_seconds: int, file_name: str | None = None) -> bytes:
    data = stream.read(CHUNK_SIZE)
    if file_name:
        save_audio_file(data, duration_in_seconds, file_name)
    stream.stop_stream()
    stream.close()
    return data

if __name__ == "__main__":
    import time
    print("Starting recording")
    start_recording_time = time.time()
    stream = start_recording()
    time.sleep(3)
    finish_recording_time = time.time()
    duration_in_seconds = int((finish_recording_time - start_recording_time))
    print("Finished recording")
    stop_recording(stream, duration_in_seconds, "audio_recording.mp3")