import json

from elevenlabs import generate, play, save  #  type: ignore[import]
# from elevenlabs import Accent, Age, Gender, Voice, VoiceDesign

# https://github.com/elevenlabs/elevenlabs-python
# https://beta.elevenlabs.io/speech-synthesis
# https://docs.elevenlabs.io/voicelab/voice-design

# Use Voice.from_design() to get a Voice object, and "upload" it
# https://github.com/elevenlabs/elevenlabs-python/blob/main/elevenlabs/api/voice.py#L78


# https://github.com/lugia19/elevenlabslib/blob/master/elevenlabslib/ElevenLabsVoice.py#LL215C73-L215C73 - Optimisation

with open("keys/eleven_labs_keys.txt", "r", encoding="utf-8") as file:
    keys = file.read().strip().split("\n")

current_index = 0

# Stability: 0.75
# Similarity Boost: 0.55

# script_text = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready! Ooming! Hang on a second. Hello? - Barry? - Adam? - Oan you believe this is happening? - I can't. I'll pick you up. Looking sharp. Use the stairs. Your father paid good money for those. Sorry. I'm excited. Here's the graduate. We're very proud of you, son. A perfect report card, all B's. Very proud. Ma! I got a thing going here. - You got lint on your fuzz. - Ow! That's me! - Wave to us! We'll be in row 118,000. - Bye! Barry, I told you, stop flying in the house! - Hey, Adam. - Hey, Barry. - Is that fuzz gel? - A little. Special day, graduation. Never thought I'd make it. Three days grade school, three days high school. Those were awkward. Three days college. I'm glad I took a day and hitchhiked around the hive. You did come back different.   - Hi, Barry. - Artie, growing a mustache? Looks good. - Hear about Frankie? - Yeah. - You going to the funeral? - No, I'm not going. Everybody knows, sting someone, you die. Don't waste it on a squirrel. Such a hothead."

VOICE_IDS = {
    "young-female-british": {
        "47823fa0792d99855b152303df37d1f0": "v68waeCuaiRz1jVfp33y",  # Dev key
        "597771e6b6e1487f988e3e7b722adc38": "LhzYJkrR4l0Xq9pcK5Bc",  # Key 1
        "6ada016287feb4ddf24af800f4f3847f": "I2m6FH4JfVIzqFpePxGU",  # Key 2
        "7f3a3a9a33955eae3390f28ebc4573a6": "2vCv0biUKuGQGx6H5LPI",  # Key 3
        "2ab74212ce3a4400fe7f60e58034f15f": "R479jMQ4qbUoaIzTsYXC",  # Key 4
        "17f5a51df733a1e4f805e4fef97b16a5": "MISSING",  # Key 5
        "5fbc24b16fd500e7e0c05702256f74bf": "MISSING",
        "61e8bc9089eec00de017f2ffc7c6217f": "MISSING",
        "d72a83e6bdf2abd761e91d2e4d34742f": "MISSING",
        "27da0659f5a5b49e1a17aee8f5ce2e32": "MISSING",
        "bf3de73de8e09bacb1c032035ddc7d22": "MISSING",  # Key 10
    }
}

# required_script = "Good evening, my name is Serenity, and I'll do my best to help you today. Why don't you introduce yourself."
# voice_design = VoiceDesign(name=f"young-female-british", text=required_script, gender=Gender.female, age=Age.young, accent=Accent.british, accent_strength=1.3, generated_voice_id=None, audio=None)
# voice = Voice.from_design(voice_design)

"""
from elevenlabs import voices, set_api_key
set_api_key(keys[3])
print([x for x in voices() if x.category != "premade"])
1/0
"""

"""
def debug_stuff():
    import time
    for i in range(100):
        print(f"{i}")
        time.sleep(1.0)
"""
USED_VOICE = VOICE_IDS["young-female-british"][keys[3]]


def convert_text_to_speech(text: str, voice_type: str, play_message: bool, pause_length: int = 0, file_name: str | None = None) -> bytes:
    """Converts text to speech using the Eleven Labs API, takes in a string, and voice type, usually `young-female-british`."""
    global current_index
    current_index = 3
    api_key = keys[current_index % len(keys)]
    # with open("keys/eleven_labs_dev_key.txt", "r") as file:
    #    api_key = file.read()

    text = text.replace(".", (". " + "-" * pause_length) if pause_length else ".").removesuffix("-" * pause_length)

    audio = generate(text=text, api_key=api_key, voice=USED_VOICE)
    audio_bytes = audio if isinstance(audio, bytes) else b"".join(audio)  # type: ignore[idk]
    if play_message:
        print("Before")
        play(audio_bytes)
        print("After")
    if file_name:
        save(audio_bytes, file_name)
    current_index += 1
    return audio_bytes


def generate_original_scripts() -> None:
    with open("assets/files/scripts.json", "r", encoding="utf-8") as file:
        all_scripts = json.load(file)

    introduction_script_text = all_scripts["introduction"].format(agent_name="Serenity")
    convert_text_to_speech(
        introduction_script_text, voice_type="young-female-british", play_message=True, file_name="assets/audio/introduction_script.mp3"
    )
    no_input_script_text = all_scripts["no_input"]
    convert_text_to_speech(
        no_input_script_text, voice_type="young-female-british", play_message=True, file_name="assets/audio/no_input_script.mp3"
    )


if __name__ == "__main__":
    # generate_original_scripts()
    # """
    import time

    start = time.time()
    # script_text = "Testing, testing"
    # """
    convert_text_to_speech(
        "This sentence should have no breaks in it. It's simply flows continuously. Here's another.",
        voice_type="young-female-british",
        play_message=False,
        pause_length=3,
        file_name="assets/audio/test.mp3",
    )
    # """
    # generate_voices()
    end = time.time()
    print(f"Time taken: {end - start}")
    # """
