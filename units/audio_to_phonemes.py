from typing import TypedDict

from allosaurus.app import read_recognizer  # type: ignore[import]
from pydub import AudioSegment  # type: ignore[import]


class PhonemeRow(TypedDict):
    timestamp: float
    duration: float
    phoneme: str


def convert_mp3_to_wav(original_file_path: str, wav_file_path: str) -> None:
    """ Converts an MP3 file to a WAV file."""
    sound = AudioSegment.from_mp3(original_file_path)
    sound.export(wav_file_path, format="wav")


def convert_audio_to_phonemes(file_path: str, convert_to_wav: bool) -> list[PhonemeRow]:
    """ Takes the name of an audio file and returns a list of phonemes with timestamps and durations."""
    if convert_to_wav:
        wav_file_path = file_path.replace(".mp3", ".wav")
        convert_mp3_to_wav(file_path, wav_file_path)
        file_path = wav_file_path

    model = read_recognizer("latest")
    data: str = model.recognize(file_path, timestamp=True)
    lines = data.split("\n")
    formatted_data: list[PhonemeRow] = [
        {"timestamp": float(line.split(" ")[0]), "duration": float(line.split(" ")[1]), "phoneme": str(line.split(" ")[2])}
        for line in lines
    ]
    return formatted_data


list_of_all_english_phonemes = ['a', 'aː', 'b', 'd', 'd̠', 'e', 'eː', 'e̞', 'f', 'h', 'i', 'iː', 'j', 'k', 'kʰ', 'l', 'm', 'n', 'o', 'oː', 'p', 'pʰ', 'r', 's', 't', 'tʰ', 't̠', 'u', 'uː', 'v', 'w', 'x', 'z', 'æ', 'ð', 'øː', 'ŋ', 'ɐ', 'ɐː', 'ɑ', 'ɑː', 'ɒ', 'ɒː', 'ɔ', 'ɔː', 'ɘ', 'ə', 'əː', 'ɛ', 'ɛː', 'ɜː', 'ɡ', 'ɪ', 'ɪ̯', 'ɯ', 'ɵː', 'ɹ', 'ɻ', 'ʃ', 'ʉ', 'ʉː', 'ʊ', 'ʌ', 'ʍ', 'ʒ', 'ʔ', 'θ']  # fmt: skip
list_of_all_phonemes = ['I', 'a', 'aː', 'ã', 'ă', 'b', 'bʲ', 'bʲj', 'bʷ', 'bʼ', 'bː', 'b̞', 'b̤', 'b̥', 'c', 'd', 'dʒ', 'dʲ', 'dː', 'd̚', 'd̥', 'd̪', 'd̯', 'd͡z', 'd͡ʑ', 'd͡ʒ', 'd͡ʒː', 'd͡ʒ̤', 'e', 'eː', 'e̞', 'f', 'fʲ', 'fʷ', 'fː', 'g', 'gʲ', 'gʲj', 'gʷ', 'gː', 'h', 'hʷ', 'i', 'ij', 'iː', 'i̞', 'i̥', 'i̯', 'j', 'k', 'kx', 'kʰ', 'kʲ', 'kʲj', 'kʷ', 'kʷʼ', 'kʼ', 'kː', 'k̟ʲ', 'k̟̚', 'k͡p̚', 'l', 'lʲ', 'lː', 'l̪', 'm', 'mʲ', 'mʲj', 'mʷ', 'mː', 'n', 'nj', 'nʲ', 'nː', 'n̪', 'n̺', 'o', 'oː', 'o̞', 'o̥', 'p', 'pf', 'pʰ', 'pʲ', 'pʲj', 'pʷ', 'pʷʼ', 'pʼ', 'pː', 'p̚', 'q', 'r', 'rː', 's', 'sʲ', 'sʼ', 'sː', 's̪', 't', 'ts', 'tsʰ', 'tɕ', 'tɕʰ', 'tʂ', 'tʂʰ', 'tʃ', 'tʰ', 'tʲ', 'tʷʼ', 'tʼ', 'tː', 't̚', 't̪', 't̪ʰ', 't̪̚', 't͡s', 't͡sʼ', 't͡ɕ', 't͡ɬ', 't͡ʃ', 't͡ʃʲ', 't͡ʃʼ', 't͡ʃː', 'u', 'uə', 'uː', 'u͡w', 'v', 'vʲ', 'vʷ', 'vː', 'v̞', 'v̞ʲ', 'w', 'x', 'x̟ʲ', 'y', 'z', 'zj', 'zʲ', 'z̪', 'ä', 'æ', 'ç', 'çj', 'ð', 'ø', 'ŋ', 'ŋ̟', 'ŋ͡m', 'œ', 'œ̃', 'ɐ', 'ɐ̞', 'ɑ', 'ɑ̱', 'ɒ', 'ɓ', 'ɔ', 'ɔ̃', 'ɕ', 'ɕː', 'ɖ̤', 'ɗ', 'ə', 'ɛ', 'ɛ̃', 'ɟ', 'ɡ', 'ɡʲ', 'ɡ̤', 'ɡ̥', 'ɣ', 'ɣj', 'ɤ', 'ɤɐ̞', 'ɤ̆', 'ɥ', 'ɦ', 'ɨ', 'ɪ', 'ɫ', 'ɯ', 'ɯ̟', 'ɯ̥', 'ɰ', 'ɱ', 'ɲ', 'ɳ', 'ɴ', 'ɵ', 'ɸ', 'ɹ', 'ɹ̩', 'ɻ', 'ɻ̩', 'ɽ', 'ɾ', 'ɾj', 'ɾʲ', 'ɾ̠', 'ʀ', 'ʁ', 'ʁ̝', 'ʂ', 'ʃ', 'ʃʲː', 'ʃ͡ɣ', 'ʈ', 'ʉ̞', 'ʊ', 'ʋ', 'ʋʲ', 'ʌ', 'ʎ', 'ʏ', 'ʐ', 'ʑ', 'ʒ', 'ʒ͡ɣ', 'ʔ', 'ʝ', 'ː', 'β', 'β̞', 'θ', 'χ', 'ә', 'ḁ']  # fmt: skip

if __name__ == "__main__":
    # import time
    # start = time.time()
    # convert_mp3_to_wav(original_file_path, wav_file_path)
    # end = time.time()
    # print("Time to convert to wav: ", end - start)
    # start = time.time()

    phonemes = convert_audio_to_phonemes(file_path="assets/audio/elevenlabs_audio_example.mp3", convert_to_wav=True)
    print(phonemes)
    for phoneme in phonemes:
        if phoneme["phoneme"] in list_of_all_phonemes and phoneme["phoneme"] not in list_of_all_english_phonemes:
            print(phoneme)
    # end = time.time()
    # print("Time to recognize: ", end - start)
