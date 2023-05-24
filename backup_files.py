# import openai
# openai.api_key

"""
messages = [{"role": "system", "content":
             "You are a virtual therapist. You will do your best to guide and advise the user on how to progress. "
             "You will ask questions about the user, especially when you're unsure of anything."}]

while True:
    message = input("User: ")
    if message:
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    convert_text_to_speech(reply, play_message=True)
    messages.append({"role": "assistant", "content": reply})
"""

"""
def get_aws_sts_assume_role_credentials():
    sts_client = boto3.client("sts")
    aws_assume_role_arn = ""

    credentials = sts_client.assume_role(
        RoleArn=aws_assume_role_arn, RoleSessionName="SessionName", DurationSeconds=42_000  # Roughly 12 hours
    )

    return credentials["Credentials"]
#aws_access_key_id, aws_secret_access_key, aws_session_token = get_aws_sts_assume_role_credentials()
"""

# self.last_agent_response = ""
# self.last_human_response = ""


"""
async def send(_ws, audio_data) -> Literal[True]:
    while True:
        try:
            data = base64.b64encode(audio_data).decode("utf-8")
            # print(f"{data=}")
            json_data = json.dumps({"audio_data": str(data)})
            await _ws.send(json_data)
        except websockets.exceptions.ConnectionClosedError as e:  # type: ignore
            print(e)
            assert e.code == 4008
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error"
        await asyncio.sleep(0.01)
    return True


async def receive(_ws) -> None:
    while True:
        try:
            result_str = await _ws.recv()
            print(json.loads(result_str)["text"])
        except websockets.exceptions.ConnectionClosedError as e:  # type: ignore
            print(e)
            assert e.code == 4008
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error"
"""

# Handle agent avatar
# self.agent_avatar.animate(self.last_agent_response_sentiment)  # Should be threaded, but currently does nothing

"""
class STTWebhookHandler:
    def __init__(self, on_receive: Callable[[str], None]) -> None:
        self.on_receive = on_receive

        URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
        self.webhook = websockets.connect(URL, extra_headers=(("Authorization", auth_key),), ping_interval=5, ping_timeout=20)  # type: ignore[attr-defined]
        self.last_send = datetime.now()

        thread = threading.Thread(target=self.keep_alive)
        thread.start()
        # #self.webhook.close()  # Somewhere, we need to close the websocket, or we can just let it die?

    async def keep_alive(self) -> None:
        if self.last_send + timedelta(seconds=55) < datetime.now():  # If the last send was more than 55 seconds ago
            asyncio.run(self.send(b""))

    async def send(self, audio_data: bytes) -> None:
        data = base64.b64encode(audio_data).decode("utf-8")
        json_data = json.dumps({"audio_data": str(data)})
        await self.webhook.send(json_data)
        self.last_send = datetime.now()

    async def receive(self) -> None:
        result_str = await self.webhook.recv()
        string = json.loads(result_str)["text"]
        self.on_receive(string)
"""

"""
    def on_error(self, _, error) -> None:
        if isinstance(error, Exception):
            print("Error: ", error)
        else:
            error_message = json.loads(error)
            print(f"{error_message=}")

"""

'''
with open("keys/aws_access_keys.txt", "r") as file:
    aws_access_key_id, aws_secret_access_key, aws_session_token = (
        *file.read().strip().split("\n"),
        None,
    )

client = boto3.client(
    "polly",
    region_name="eu-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
)


def convert_text_to_speech(message: str, play_message: bool) -> None:
    """Convert text to speech using AWS Polly, and play the message if play_message is True"""
    response = client.synthesize_speech(
        Engine="neural",
        LanguageCode="en-GB",
        # "LexiconNames"=[ "string" ],
        OutputFormat="mp3",
        # "SampleRate"="string",
        # SpeechMarkTypes"=[ "string" ],
        Text=message,
        TextType="text",
        VoiceId="Amy",
    )
    streaming_body = response["AudioStream"]
    with open("assets/audio/main.mp3", "wb") as file:
        file.write(streaming_body.read())
    if play_message:
        playsound("assets/audio/main.mp3")
'''

"""
class STTHandler:
    def __init__(self, on_receive: Callable[[str], None]) -> None:
        self.on_receive = on_receive
        self.queue: list[bytes] = []

        thread = Thread(target=lambda: asyncio.run(self.handle_socket()))
        thread.start()

    async def handle_socket(self) -> None:
        deepgram = Deepgram(DEEPGRAM_API_KEY)
        print("Here")
        self.socket: LiveTranscription = await deepgram.transcription.live(API_SETTINGS)  
        print("Post")
        event: LiveTranscriptionEvent = self.socket.event  # type: ignore[attr-defined]
        self.socket.registerHandler(event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        self.socket.registerHandler(event.TRANSCRIPT_RECEIVED, self.on_receive)

    def close(self) -> None:
        asyncio.run(self.socket.finish())

    def while_running(self) -> None:
        while True:
            if self.queue:
                audio_data = self.queue.pop(0)
                print("Sending data")
                self.socket.send(audio_data)
    
    def send(self, audio_data: bytes) -> None:
        self.queue.append(audio_data)
"""

if __name__ == "__main__" and False:
    print("Before initialisation of STTHandler")
    stt_handler = STTHandler(print)
    import time
    time.sleep(5)
    with open("assets/audio/test.mp3", "rb") as file:
        stt_handler.send(file.read())
    print("post")

"""
{
  "channel_index": [0, 1],
  "duration": 2.0900002,
  "start": 7.04,
  "is_final": true,
  "speech_final": true,
  "channel": {
    "alternatives": [
      {
        "transcript": "I said it before, and I'll say it again.",
        "confidence": 0.9896645,
        "words": [
          {
            "word": "i",
            "start": 7.2599998,
            "end": 7.46,
            "confidence": 0.8708194,
            "punctuated_word": "I"
          },
          {
            "word": "said",
            "start": 7.46,
            "end": 7.58,
            "confidence": 0.9085592,
            "punctuated_word": "said"
          },
          ...
        ]
      }
    ]
  },
  "metadata": {
    "request_id": "4d9a5590-fe66-46f1-81d5-a95b9140ac04",
    "model_uuid": "41757536-6114-494d-83fd-c2694524d80b"
  }
}
"""

'''
    def on_receive(self, text: str) -> None:
        """Runs when the STTWebhookHandler receives a new text from the API."""
        print("Received text from API:", text)
        self.current_monolog_text = text
    '''

"""
def generate_voices() -> None:
    raise NotImplementedError
    for key in keys:
        set_api_key(key)
        required_script = "Good evening, my name is Serenity, and I'll do my best to help you today. Why don't you introduce yourself."
        voice_design = VoiceDesign(name=f"{key}-female-british", text=required_script, gender=Gender.female, age=Age.young, accent=Accent.british, accent_strength=1.3, generated_voice_id=None, audio=None)
        voice_design.generate()
        print(f'        "{key}": "{voice_design.generated_voice_id}",')
"""

"""
import wave
from datetime import datetime

from speech_to_text import STTWebhookHandler
from new_STT_exp import STTHandler

CHUNK_SIZE = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Amount of bits per second
p = pyaudio.PyAudio()
ONE_SECONDS_WORTH = RATE


class AudioRecordingHandler:

    def __init__(self) -> None:
        self.stream: pyaudio.Stream | None = None
        self.frames: list[bytes] = []  # Each frame should be 1 second of audio
        # self.speech_to_text_wh_handler = STTWebhookHandler(self.on_receive)
        self.speech_to_text_wh_handler = STTHandler(self.on_receive)
        self.current_monolog_text = ""

    def on_receive(self, text: str) -> None:
       
        print("Received text from API:", text)
        self.current_monolog_text = text

    def save_one_second(self) -> None:
       
        while True:
            if self.stream is None:
                return
            start_time = datetime.now()
            try:
                frame = self.stream.read(ONE_SECONDS_WORTH)
                self.frames.append(frame)
            except OSError:  # OSError: [Errno -9981] Input overflowed
                return

            end_time = datetime.now()
            time_taken = (end_time - start_time).total_seconds()
            if time_taken < 1:
                time.sleep(1 - time_taken)
            self.speech_to_text_wh_handler.send(frame)

    def start_recording(self) -> None:
       
        stream: pyaudio._Stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )
        self.stream = stream

        thread = threading.Thread(target=self.save_one_second)
        thread.start()

    def stop_recording(self, file_name: str | None = None) -> str:
       
        time.sleep(0.5)  # This is to make sure the chunks don't get truncated early
        assert self.stream is not None
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        time.sleep(0.5)  # To wait for the remaining webhooks to come in
        complete_recording = b"".join(self.frames)
        if file_name:
            self.save_audio_file(complete_recording, file_name)
        print(f"{self.current_monolog_text=}")
        return self.current_monolog_text

    def save_audio_file(self, complete_recording: bytes, file_name: str) -> None:
        
        print("Saving audio file as", file_name)
        sample_size = p.get_sample_size(FORMAT)

        with wave.open(file_name, "wb") as file:
            file.setnchannels(CHANNELS)
            file.setsampwidth(sample_size)
            file.setframerate(RATE)
            file.writeframes(complete_recording)
        print("Post saving file (won't happen normally))")


if __name__ == "__main__":
    audio_handler = AudioRecordingHandler()
    print("Start recording!")
    audio_handler.start_recording()
    time.sleep(5)
    print("Slept 5 seconds")
    print("Stop recording!")
    audio_handler.stop_recording("assets/audio/test.wav")
    print(audio_handler.current_monolog_text)
"""