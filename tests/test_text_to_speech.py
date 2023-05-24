# import pytest
from text_to_speech import convert_text_to_speech

TEST_PROMPT_1 = "This is a test of text to speech, while it doesn't test the actual content of the return mp3 file/audio data, it does test to see if the function errors at any point."
TEST_PROMPT_2 = "I've been very depressed lately, and because of that, I'm becoming more isolated, which makes me lonely, which then makes my depression worse. I'm not sure what I can do to improve things."


def test_text_to_speech_failure_1() -> None:
    assert convert_text_to_speech(TEST_PROMPT_1, False) is not None  # type: ignore[func-returns-value]


def test_text_to_speech_failure_2() -> None:  # Example sentence
    assert convert_text_to_speech(TEST_PROMPT_2, False) is not None  # type: ignore[func-returns-value]
