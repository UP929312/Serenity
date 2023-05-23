from deepgram import Deepgram
from deepgram.transcription import LiveTranscription
from deepgram._types import LiveOptions
from deepgram._enums import LiveTranscriptionEvent

import asyncio
from typing import Callable
from threading import Thread

with open("keys/deepgram_key.txt", "r") as f:
    DEEPGRAM_API_KEY = f.read()

API_SETTINGS = LiveOptions(punctuate=True, interim_results=False, language='en-GB', model='nova')

class STTHandler:
    def __init__(self, on_receive: Callable[[str], None]) -> None:
        self.on_receive = on_receive

        #thread = Thread(target=lambda: self.webhook.run_forever())
        #thread.start()
        asyncio.run(self.handle_socket())

    async def handle_socket(self) -> None:
        self.current_message = ""
        deepgram = Deepgram(DEEPGRAM_API_KEY)
        print("Here")
        self.socket: LiveTranscription = await deepgram.transcription.live(API_SETTINGS)  
        print("Post")
        event: LiveTranscriptionEvent = self.socket.event  # type: ignore[attr-defined]
        self.socket.registerHandler(event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
        self.socket.registerHandler(event.TRANSCRIPT_RECEIVED, self.on_receive)

    def send(self, audio_data: bytes) -> None:
        print("Sending data")
        self.socket.send(audio_data)

stt_handler = STTHandler(print)
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