import boto3
from playsound import playsound

"""
def get_aws_sts_assume_role_credentials():
    sts_client = boto3.client("sts")
    aws_assume_role_arn = "arn:aws:iam::025756472661:user/main_user"

    credentials = sts_client.assume_role(
        RoleArn=aws_assume_role_arn, RoleSessionName="SessionName", DurationSeconds=42_000  # Roughly 12 hours
    )

    return credentials["Credentials"]
#aws_access_key_id, aws_secret_access_key, aws_session_token = get_aws_sts_assume_role_credentials()
"""
with open("aws_access_keys.txt", "r") as file:
    aws_access_key_id, aws_secret_access_key = file.read().strip().split("\n")
aws_session_token = None

client = boto3.client('polly', region_name="eu-west-2", aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

def convert_text_to_speech(message: str, play_message: bool) -> None:
    response = client.synthesize_speech(    
       Engine="neural",
       LanguageCode="en-GB",
       #"LexiconNames"=[ "string" ],
       OutputFormat="mp3",
       #"SampleRate"="string",
       #SpeechMarkTypes"=[ "string" ],
       Text=message,
       TextType="text",
       VoiceId="Amy"
    )
    streaming_body = response["AudioStream"]
    with open("main.mp3", "wb") as file:
        file.write(streaming_body.read())
    if play_message:
        playsound("main.mp3")
    return
