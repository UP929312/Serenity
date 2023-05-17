
# https://www.assemblyai.com/docs/Models/entity_detection

import websockets
import asyncio
import base64
import json

from pyaudio_interface import stream, FRAMES_PER_BUFFER

with open("keys/assemblyai_key.txt", "r") as file:
    auth_key = file.read()

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

# "format_text": False  <- Removes punctuation, to stop sentences being broken up incorrectly
# "disfluencies": True  <- Keeps the "ums" and "uhs"

async def send(_ws):
    while True:
        try:
            data = stream.read(FRAMES_PER_BUFFER)

            data = base64.b64encode(data).decode("utf-8")
            #print(f"{data=}")
            json_data = json.dumps({"audio_data": str(data)})
            await _ws.send(json_data)
        except websockets.exceptions.ConnectionClosedError as e:
            print(e)
            assert e.code == 4008
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error"
        await asyncio.sleep(0.01)
    return True

async def receive(_ws):
    while True:
        try:
            result_str = await _ws.recv()
            print(json.loads(result_str)['text'])
        except websockets.exceptions.ConnectionClosedError as e:
            print(e)
            assert e.code == 4008
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error"
      

async def send_receive():
   print(f'Connecting websocket to url ${URL}')

   async with websockets.connect(URL, extra_headers=(("Authorization", auth_key),), ping_interval=5, ping_timeout=20) as _ws:
       await asyncio.sleep(0.1)
       await _ws.recv()
       send_result, receive_result = await asyncio.gather(send(_ws), receive(_ws))

#while True:
#    asyncio.run(send_receive())

async def convert_speech_to_text():
    asyncio.run(send_receive())