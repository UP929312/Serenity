import pyaudio

FRAMES_PER_BUFFER = int(3200)
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
)

from keyboard_detection import check_if_pressing_v

while True:
    if check_if_pressing_v():
        print("V pressed")
        stream.read(FRAMES_PER_BUFFER)
