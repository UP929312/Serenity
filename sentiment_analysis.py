import boto3

with open("keys/aws_access_keys.txt", "r") as file:
    aws_access_key_id, aws_secret_access_key, aws_session_token = (*file.read().strip().split("\n"), None)

comprehend = boto3.client('comprehend', region_name="eu-west-2", aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

def detect_sentiment(text) -> dict[str, str|int]:
    data = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return {"sentiment": data["Sentiment"], "confidence": data["SentimentScore"][data["Sentiment"].title()]}

if __name__ == "__main__":
    sentiment = detect_sentiment("I hate life, it keeps pulling me down")
    print(sentiment)
    sentiment = detect_sentiment("I really enjoy these sessions, they're so much fun and helpful")
    print(sentiment)
    