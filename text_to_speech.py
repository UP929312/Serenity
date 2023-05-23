from elevenlabs import generate, set_api_key, save, play  # , voices
import json

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

#script_text = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready! Ooming! Hang on a second. Hello? - Barry? - Adam? - Oan you believe this is happening? - I can't. I'll pick you up. Looking sharp. Use the stairs. Your father paid good money for those. Sorry. I'm excited. Here's the graduate. We're very proud of you, son. A perfect report card, all B's. Very proud. Ma! I got a thing going here. - You got lint on your fuzz. - Ow! That's me! - Wave to us! We'll be in row 118,000. - Bye! Barry, I told you, stop flying in the house! - Hey, Adam. - Hey, Barry. - Is that fuzz gel? - A little. Special day, graduation. Never thought I'd make it. Three days grade school, three days high school. Those were awkward. Three days college. I'm glad I took a day and hitchhiked around the hive. You did come back different.   - Hi, Barry. - Artie, growing a mustache? Looks good. - Hear about Frankie? - Yeah. - You going to the funeral? - No, I'm not going. Everybody knows, sting someone, you die. Don't waste it on a squirrel. Such a hothead."

def convert_text_to_speech(text: str, play_message: bool, file_name: str | None = None) -> bytes:
    global current_index
    api_key = keys[current_index % len(keys)]
    set_api_key(api_key)
    audio = generate(text=text, voice="v68waeCuaiRz1jVfp33y")
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
    convert_text_to_speech(script_text, False, "assets/audio/test.mp3")
    end = time.time()
    print(f"Time taken: {end - start}")

