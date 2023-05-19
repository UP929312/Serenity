# import pytest
from text_to_speech import convert_text_to_speech


def test_text_to_speech_failure_1() -> None:
    assert (
        convert_text_to_speech(
            "This is a test of text to speech, while it doesn't test the actual content of the return mp3 file/audio data, it does test to see if the function errors at any point.",
            False,
        )
        == None
    )


def test_text_to_speech_failure_2() -> None:  # Example sentence
    assert (
        convert_text_to_speech(
            "I've been very depressed lately, and because of that, I'm becoming more isolated, which makes me lonely, which then makes my depression worse. I'm not sure what I can do to improve things.",
            False,
        )
        == None
    )
