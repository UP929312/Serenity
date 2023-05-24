import json

from elevenlabs import Accent, Age, Gender, Voice, VoiceDesign, generate, play, save, set_api_key  #  type: ignore[import]

# https://github.com/elevenlabs/elevenlabs-python
# https://beta.elevenlabs.io/speech-synthesis
# https://docs.elevenlabs.io/voicelab/voice-design

with open("keys/eleven_labs_keys.txt", "r") as file:
    keys = file.read().strip().split("\n")

current_index = 0

# Stability: 0.75
# Similarity Boost: 0.55

with open("assets/files/introduction_script.json", "r") as file:
    script_text = json.load(file)["introduction"]
    script_text = script_text.format(name="Katrina", agent_name="Serenity")

# script_text = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready! Ooming! Hang on a second. Hello? - Barry? - Adam? - Oan you believe this is happening? - I can't. I'll pick you up. Looking sharp. Use the stairs. Your father paid good money for those. Sorry. I'm excited. Here's the graduate. We're very proud of you, son. A perfect report card, all B's. Very proud. Ma! I got a thing going here. - You got lint on your fuzz. - Ow! That's me! - Wave to us! We'll be in row 118,000. - Bye! Barry, I told you, stop flying in the house! - Hey, Adam. - Hey, Barry. - Is that fuzz gel? - A little. Special day, graduation. Never thought I'd make it. Three days grade school, three days high school. Those were awkward. Three days college. I'm glad I took a day and hitchhiked around the hive. You did come back different.   - Hi, Barry. - Artie, growing a mustache? Looks good. - Hear about Frankie? - Yeah. - You going to the funeral? - No, I'm not going. Everybody knows, sting someone, you die. Don't waste it on a squirrel. Such a hothead."

"""
VOICE_IDS = {
    "young-female-british": {
        "47823fa0792d99855b152303df37d1f0": "v68waeCuaiRz1jVfp33y",  # Dev key
        "597771e6b6e1487f988e3e7b722adc38": "LhzYJkrR4l0Xq9pcK5Bc",  # Key 1
        "6ada016287feb4ddf24af800f4f3847f": "SfKmsTU50DBIkJKZcMD5",
        "7f3a3a9a33955eae3390f28ebc4573a6": "ha5SnxjwaBKKKgGtDUEI",
        "2ab74212ce3a4400fe7f60e58034f15f": "jyyGRGxvg37zYhYl30bi",
        "17f5a51df733a1e4f805e4fef97b16a5": "HlGPwf3BegyWwJLdrQak",  # Key 5
        "5fbc24b16fd500e7e0c05702256f74bf": "EtDuKIvgCWo672ly9PgS",
        "61e8bc9089eec00de017f2ffc7c6217f": "DNeMtCJBGfIZ3uCA9xLG",
        "d72a83e6bdf2abd761e91d2e4d34742f": "wDdG57rbH3g76uJwX2bP",
        "27da0659f5a5b49e1a17aee8f5ce2e32": "b3YgAeuXNKUU7GrnhUbx",
        "bf3de73de8e09bacb1c032035ddc7d22": "QHZSiqPrELV6jWDGZXGP",  # Key 10
    }
}
"""

# required_script = "Good evening, my name is Serenity, and I'll do my best to help you today. Why don't you introduce yourself."
# voice_design = VoiceDesign(name=f"young-female-british", text=required_script, gender=Gender.female, age=Age.young, accent=Accent.british, accent_strength=1.3, generated_voice_id=None, audio=None)
# voice = Voice.from_design(voice_design)


def convert_text_to_speech(text: str, voice_type: str, play_message: bool, file_name: str | None = None) -> bytes:
    """Converts text to speech using the Eleven Labs API, takes in a string, and voice type, usually `young-female-british`."""
    global current_index
    # api_key = keys[current_index % len(keys)]
    api_key = open("keys/eleven_labs_dev_key.txt", "r").read()
    # print(api_key)
    # api_key = keys[6 % len(keys)]
    set_api_key(api_key)

    audio = generate(text=text, voice="v68waeCuaiRz1jVfp33y")  # voice)#VOICE_IDS[voice_type][api_key])
    audio_bytes = audio if isinstance(audio, bytes) else b"".join(audio)
    if play_message:
        play(audio_bytes)
    if file_name:
        save(audio_bytes, "assets/audio/test.mp3")
    current_index += 1
    return audio_bytes


if __name__ == "__main__":
    import time

    start = time.time()
    script_text = "Testing, testing"
    convert_text_to_speech(script_text, voice_type="young-female-british", play_message=True, file_name="assets/audio/test.mp3")
    # generate_voices()
    end = time.time()
    print(f"Time taken: {end - start}")
