import pyaudio
 
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

def start_recording() -> pyaudio.Stream:
    stream: pyaudio._Stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )
    return stream

def stop_recording(stream: pyaudio.Stream) -> bytes:
    data = stream.read(FRAMES_PER_BUFFER)
    stream.stop_stream()
    stream.close()
    return data