from datetime import datetime, timedelta
from typing import Callable
import websocket  # type: ignore[import]
import base64
import json
import threading

with open("keys/assemblyai_key.txt", "r") as file:
    auth_key = file.read()

headers = {"Authorization": auth_key}
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# https://www.assemblyai.com/docs/Models/entity_detection
# https://www.assemblyai.com/docs/Guides/real-time_streaming_transcription

# "format_text": False  <- Removes punctuation, to stop sentences being broken up incorrectly
# "disfluencies": True  <- Keeps the "ums" and "uhs"

# Current plan:
# We need to create a permanent webhook that keeps itself alive, and then we need to chunk up the audio data, one-two frames at a time, and send it to the websocket.
# We then need to somehow combine the text inputs, but we might have to send the audio as they come in, potentially by giving the recording handler a callback?
# To not die, it must send audio at least once every second, so we probably need a function that sends empty sound for 1 second every minute, cost wise, not sure how this will work?

# https://stackoverflow.com/a/69109651/10177123

# We have an ID for each session right, so we can join on ID?



# https://developers.deepgram.com/docs/getting-started-with-live-streaming-audio
# Use this instead...

class STTWebhookHandler:
    """
    A class that handles the websocket connection to AssemblyAI's Speech to Text API. It sends audio data to the API and receives text data back.\n
    It also keeps the connection alive by sending empty audio data every minute.\n
    It also has a callback function, `on_receive`, that is called whenever a new text is received from the API.
    """

    def __init__(self, on_receive: Callable[[str], None]) -> None:
        self.on_receive = on_receive

        self.webhook = websocket.WebSocketApp(URL, header=headers, on_message=self.on_message_receive)
        self.last_send = datetime.now()

        thread = threading.Thread(target=self.keep_alive)
        thread.start()
        thread2 = threading.Thread(target=lambda: self.webhook.run_forever())
        thread2.start()

        self.webhook_ids: dict[datetime, str] = {}

    def keep_alive(self) -> None:
        """
        A function that sends empty audio data every minute to keep the connection alive.\n
        This function runs in a separate thread, so won't affect the main loop.
        """
        print("Ah, ah, ah, ah, staying alive, staying alive")
        if self.last_send + timedelta(seconds=55) < datetime.now():  # If the last send was more than 55 seconds ago
            self.webhook.send('{"audio_data": ""}')
            self.last_send = datetime.now()

    def send(self, audio_data: bytes) -> None:
        # print("Webhook is sending some data")
        data = base64.b64encode(audio_data).decode("utf-8")
        json_data = json.dumps({"audio_data": str(data)})
        self.webhook.send(json_data)
        self.last_send = datetime.now()

    def on_message_receive(self, _: websocket.WebSocketApp, message_raw: str) -> None:
        """Fires when a message is received from the websocket (containing a dictionary, including the text)."""
        message = json.loads(message_raw)
        # print(f"{message=}")
        # if message["message_type"] == "SessionBegins":
        # session_id = message["session_id"]
        # expires_at = message["expires_at"]
        if message["message_type"] == "PartialTranscript":
            if message["text"] != "":
                #print(message)
                self.webhook_ids[message["created"]] = message["text"]

                print(f"Partial transcript received: {message['text']}")
                self.on_receive(message["text"])
        if message["message_type"] == "FinalTranscript":
            print(f"Final transcript received: {message['text']}")
            self.on_receive(message["text"])


if __name__ == "__main__":
    handler = STTWebhookHandler(lambda x: print(x))
    while True:
        pass
