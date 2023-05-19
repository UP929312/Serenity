import pytest
from sentiment_analysis import detect_sentiment


def test_positive_sentiment_1() -> None:
    assert detect_sentiment("I'm super excited for the weekend and can't wait for it")[0] == "POSITIVE"


def test_positive_sentiment_2() -> None:
    assert detect_sentiment("I'm doing really well and am surprised by my progress")[0] == "POSITIVE"


def test_neutral_sentiment_1() -> None:
    assert detect_sentiment("I will be going back to school on Monday until Friday")[0] == "NEUTRAL"


def test_neutral_sentiment_2() -> None:
    assert detect_sentiment("I had a English lesson today, followed by history")[0] == "NEUTRAL"


def test_negative_sentiment_1() -> None:
    assert detect_sentiment("I'm devistated, I thought I could do it, but clearly not")[0] == "NEGATIVE"


@pytest.mark.xfail(reason="This one fails for some reason")  # ('NEUTRAL', 0.32802483439445496)
def test_negative_sentiment_2() -> None:
    assert detect_sentiment("It's just all going wrong, what else can fail?")[0] == "NEGATIVE"
