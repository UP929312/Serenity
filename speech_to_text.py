from datetime import datetime, timedelta
from typing import Callable
import websocket
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


class STTWebhookHandler:
    def __init__(self, on_receive: Callable[[str], None]) -> None:
        self.on_receive = on_receive

        self.webhook = websocket.WebSocketApp(URL, header=headers, on_message=self.on_message, on_error=self.on_error)
        self.last_send = datetime.now()

        thread = threading.Thread(target=self.keep_alive)
        thread.start()
        thread2 = threading.Thread(target=lambda: self.webhook.run_forever())
        thread2.start()

    def keep_alive(self) -> None:
        print("Ah, ah, ah, ah, staying alive, staying alive")
        if self.last_send + timedelta(seconds=55) < datetime.now():  # If the last send was more than 55 seconds ago
            self.webhook.send('{"audio_data": ""}')

    def send(self, audio_data: bytes) -> None:
        # print("Webhook is sending some data")
        data = base64.b64encode(audio_data).decode("utf-8")
        json_data = json.dumps({"audio_data": str(data)})
        self.webhook.send(json_data)
        self.last_send = datetime.now()

    def on_message(self, ws, message_raw) -> None:
        message = json.loads(message_raw)
        # print(f"{message=}")
        if False:
            pass
            # if message["message_type"] == "SessionBegins":
            # session_id = message["session_id"]
            # expires_at = message["expires_at"]
            # print(f"Session ID: {session_id}")
            # print(f"Expires at: {expires_at}")
        elif message["message_type"] == "PartialTranscript":
            if message["text"] != "":
                print(f"Partial transcript received: {message['text']}")
                self.on_receive(message["text"])
        # if message['message_type'] == 'FinalTranscript':
        #     print(f"Final transcript received: {message['text']}")
        #     self.on_receive(message["text"])

    def on_error(self, ws, error) -> None:
        error_message = json.loads(error)
        print(f"{error_message=}")


if __name__ == "__main__":

    def on_receive(string: str) -> None:
        print("Received: ", string)

    handler = STTWebhookHandler(on_receive)
    while True:
        # import time
        # time.sleep(10)
        pass
