# https://www.assemblyai.com/docs/Models/entity_detection

import websockets
import asyncio
import base64
import json

from typing import Literal

# from pyaudio_interface import FRAMES_PER_BUFFER

with open("keys/assemblyai_key.txt", "r") as file:
    auth_key = file.read()

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# "format_text": False  <- Removes punctuation, to stop sentences being broken up incorrectly
# "disfluencies": True  <- Keeps the "ums" and "uhs"


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


async def send_receive(audio_data: bytes):
    print(f"Connecting websocket to url ${URL}")

    async with websockets.connect(URL, extra_headers=(("Authorization", auth_key),), ping_interval=5, ping_timeout=20) as _ws:  # type: ignore[attr-defined]
        await asyncio.sleep(0.1)
        await _ws.recv()
        send_result, receive_result = await asyncio.gather(send(_ws, audio_data), receive(_ws))


# while True:
#    asyncio.run(send_receive())


async def convert_speech_to_text(audio_data: bytes) -> str:
    asyncio.run(send_receive(audio_data))
    return "I NEVER UPDATED THIS, AHH"
