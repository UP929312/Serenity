from datetime import datetime, timedelta

import websockets
import asyncio
import base64
import json
import threading

with open("keys/assemblyai_key.txt", "r") as file:
    auth_key = file.read()

# https://www.assemblyai.com/docs/Models/entity_detection
# https://www.assemblyai.com/docs/Guides/real-time_streaming_transcription

# "format_text": False  <- Removes punctuation, to stop sentences being broken up incorrectly
# "disfluencies": True  <- Keeps the "ums" and "uhs"

# Current plan:
# We need to create a permanent webhook that keeps itself alive, and then we need to chunk up the audio data, one-two frames at a time, and send it to the websocket.
# We then need to somehow combine the text inputs, but we might have to send the audio as they come in, potentially by giving the recording handler a callback?
# To not die, it must send audio at least once every second, so we probably need a function that sends empty sound for 1 second every minute, cost wise, not sure how this will work?

class STTWebhookHandler:
    def __init__(self) -> None:
        URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
        self.webhook = websockets.connect(URL, extra_headers=(("Authorization", auth_key),), ping_interval=5, ping_timeout=20)  # type: ignore[attr-defined]
        self.last_send = datetime.now()

        thread = threading.Thread(target=self.keep_alive)
        thread.start()
        # #self.webhook.close()  # Somewhere, we need to close the websocket, or we can just let it die?

    async def keep_alive(self) -> None:
        if self.last_send + timedelta(seconds=55) < datetime.now():  # If the last send was more than 55 seconds ago
            await self.send(b"")

    async def send(self, audio_data: bytes) -> None:
        data = base64.b64encode(audio_data).decode("utf-8")
        json_data = json.dumps({"audio_data": str(data)})
        await self.webhook.send(json_data)
        self.last_send = datetime.now()

    async def receive(self) -> None:
        result_str = await self.webhook.recv()
        print(json.loads(result_str)["text"])

'''
async def send(_ws, audio_data) -> None:
    while True:
        data = base64.b64encode(audio_data).decode("utf-8")
        json_data = json.dumps({"audio_data": str(data)})
        await _ws.send(json_data)

async def receive(_ws) -> None:
    while True:
        result_str = await _ws.recv()
        print(json.loads(result_str)["text"])

async def send_receive(audio_data: bytes):
    print("Connecting to websocket")

    async with websockets.connect(URL, extra_headers=(("Authorization", auth_key),), ping_interval=5, ping_timeout=20) as _ws:  # type: ignore[attr-defined]
        await asyncio.sleep(0.1)
        test = await _ws.recv()  # Initial recieve, probably just a "connected" message
        print(test)
        await asyncio.gather(send(_ws, audio_data), receive(_ws))
'''

# while True:
#     asyncio.run(send_receive())


"""
Idle Sessions - Sessions that do not receive audio within 1 minute will be terminated.
Audio Sampling Rate Limit - Customers must send data in near real-time. If a client sends data faster than 1 second of audio per second for longer than 1 minute, we will terminate the session.


import json
from urllib.parse import urlencode

sample_rate = 16000
word_boost = ["foo", "bar"]
params = {"sample_rate": sample_rate, "word_boost": json.dumps(word_boost)}

url = f"wss://api.assemblyai.com/v2/realtime/ws?{urlencode(params)}"
"""

#async def convert_speech_to_text(audio_data: bytes) -> str:
#    asyncio.run(send_receive(audio_data))
#    return "I NEVER UPDATED THIS, AHH"
