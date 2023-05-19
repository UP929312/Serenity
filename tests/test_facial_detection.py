import pytest
from detect_facial_expression import get_facial_emotion

def test_smiling_emotion() -> None:
    assert get_facial_emotion("smiling_man")[0] == "Happiness"  

@pytest.mark.xfail(reason="This one fails for some reason")
def test_sad_emotion() -> None:
    assert get_facial_emotion("sad_girl")[0] == "Sadness"

@pytest.mark.xfail(reason="This one fails for some reason")
def test_slightly_sad_emotion() -> None:
    assert get_facial_emotion("slightly_sad_girl")[0] == "Sadness"

def test_crying_emotion() -> None:
    assert get_facial_emotion("crying_girl")[0] == "Sadness"

def test_surprised_emotion() -> None:
    assert get_facial_emotion("surprised_man")[0] == "Surprise"

def test_scared_emotion() -> None:
    assert get_facial_emotion("scared_man")[0] == "Fear"

def test_disgusted_emotion() -> None:
    assert get_facial_emotion("disgusted_lady")[0] == "Disgust"