from allosaurus.app import read_recognizer
from pydub import AudioSegment

original_file_path = "assets/audio/main.mp3"
wav_file_path = "assets/audio/main.wav"

model = read_recognizer("latest")
sound = AudioSegment.from_mp3(original_file_path)
sound.export(wav_file_path, format="wav")
with open(wav_file_path, "rb") as f:
    audio_file = f.read()
data = model.recognize(audio_file)
print(data)