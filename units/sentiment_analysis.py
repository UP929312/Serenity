from typing import Literal
import boto3

with open("keys/aws_access_keys.txt", "r", encoding="utf-8") as file:
    aws_access_key_id, aws_secret_access_key = (*file.read().strip().split("\n"),)

comprehend = boto3.client(
    "comprehend",
    region_name="eu-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=None,
)

sentiment_types = Literal["POSITIVE"] | Literal["NEGATIVE"] | Literal["NEUTRAL"] | Literal["MIXED"]


def detect_sentiment(text: str) -> tuple[sentiment_types, int]:
    """
    Takes a setence and returns the sentiment and the confidence of that sentiment, will be one of: \n
    "POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED", accurate to 2 decimal places.
    """
    if text == "":
        return "NEUTRAL", 0
    # print(f"{text=} in detect sentiment")
    data = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    sentiment_name: sentiment_types = data["Sentiment"]
    sentiment_score = round(data["SentimentScore"][sentiment_name.title()], 2)
    return sentiment_name, sentiment_score
