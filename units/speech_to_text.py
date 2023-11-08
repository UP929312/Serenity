import time
from typing import TypedDict

from deepgram import Deepgram  # type: ignore[import]
from deepgram._types import BufferSource  # type: ignore[import]
from deepgram.transcription import PrerecordedOptions, PrerecordedTranscriptionResponse # type: ignore[import]


with open("keys/deepgram_key.txt", "r") as f:
    DEEPGRAM_API_KEY = f.read()

# keywords=['first:5', 'second']
# keywords=["Serenity", "sad", "depressed", "feelings", "thoughts"]
# Detect entities and sentiment make this take from 1-2 second up to 4-8 seconds, rip
API_SETTINGS = PrerecordedOptions(
    punctuate=True, model="nova", language="en-GB"
)  # , detect_entities=True)#, sentiment=True)  # "fr" for french


class Entity(TypedDict):
    label: str
    value: str
    confidence: float


class STTHandler:
    """A class which handles the interface between the application and Deepgram's STT API"""

    def __init__(self, time_transcription: bool = False) -> None:
        self.deepgram = Deepgram(DEEPGRAM_API_KEY)
        self.time_transcription = time_transcription

    def extract_entities(self, response: PrerecordedTranscriptionResponse) -> list[Entity]:
        """ Takes a list of entities from the Deepgram API and returns a list of entities with type Entity"""
        entities_raw = response["results"]["channels"][0]["alternatives"][0].get("entities", [])  # type: ignore[params]
        entities: list[Entity] = [{"label": entity["label"]} for entity in entities_raw]  # type: ignore[type]
        return entities

    def transcribe(self, audio_data: bytes, include_entity_detection: bool=False) -> tuple[str, list[Entity]]:
        """Takes a byte string of audio data and returns the transcription as a string using Deepgram's API"""
        if len(audio_bytes) < 10:
            raise Exception("Audio data is too short to transcribe")
        source: BufferSource = {"buffer": audio_bytes, "mimetype": "audio/mp3"}
        transcription_start_time = time.time()
        response = self.deepgram.transcription.sync_prerecorded(source, option=API_SETTINGS | {"detect_entities": include_entity_detection})
        assert "results" in response
        raw_text: str = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        entities = self.extract_entities(response) if include_entity_detection else []
        if self.time_transcription:
            print(f"Transcription took {round(time.time()-transcription_start_time, 2)} seconds")
        # if raw_text == "":
        #    raise Exception("Transcription failed, and had empty text")
        return raw_text, entities
        # print(json.dumps(response, indent=4))  # Formats the response nicely


if __name__ == "__main__":
    file_name = "assets/audio/input_test.mp3"
    with open(file_name, "rb") as file:
        audio_bytes = file.read()
    text, entities = STTHandler(time_transcription=True).transcribe(audio_bytes)
    print(text)
