import boto3
from playsound import playsound

with open("keys/aws_access_keys.txt", "r") as file:
    aws_access_key_id, aws_secret_access_key, aws_session_token = (
        *file.read().strip().split("\n"),
        None,
    )

client = boto3.client(
    "polly",
    region_name="eu-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
)


def convert_text_to_speech(message: str, play_message: bool) -> None:
    response = client.synthesize_speech(
        Engine="neural",
        LanguageCode="en-GB",
        # "LexiconNames"=[ "string" ],
        OutputFormat="mp3",
        # "SampleRate"="string",
        # SpeechMarkTypes"=[ "string" ],
        Text=message,
        TextType="text",
        VoiceId="Amy",
    )
    streaming_body = response["AudioStream"]
    with open("main.mp3", "wb") as file:
        file.write(streaming_body.read())
    if play_message:
        playsound("main.mp3")
