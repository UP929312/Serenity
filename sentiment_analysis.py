import boto3

with open("keys/aws_access_keys.txt", "r", encoding="utf-8") as file:
    aws_access_key_id, aws_secret_access_key, aws_session_token = (
        *file.read().strip().split("\n"),
        None,
    )

comprehend = boto3.client(
    "comprehend",
    region_name="eu-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
)


def detect_sentiment(text: str) -> tuple[str, int]:
    """
    Takes a setence and returns the sentiment and the confidence of that sentiment, will be one of: \n
    "POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED"
    """
    # print(f"{text=} in detect sentiment")
    data = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = data["Sentiment"]
    return sentiment, data["SentimentScore"][sentiment.title()]


if __name__ == "__main__":
    sentiment = detect_sentiment("I hate life, it keeps pulling me down")
    print(sentiment)
    sentiment = detect_sentiment("I really enjoy these sessions, they're so much fun and helpful")
    print(sentiment)
    sentiment = detect_sentiment("Things are going okay today")
    print(sentiment)
    sentiment = detect_sentiment("I'm feeling very sad down today but I'm super happy too")
    print(sentiment)
