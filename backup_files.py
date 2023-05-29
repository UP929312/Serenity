"""
def get_aws_sts_assume_role_credentials():
    sts_client = boto3.client("sts")
    aws_assume_role_arn = ""

    credentials = sts_client.assume_role(
        RoleArn=aws_assume_role_arn, RoleSessionName="SessionName", DurationSeconds=42_000  # Roughly 12 hours
    )

    return credentials["Credentials"]
#aws_access_key_id, aws_secret_access_key, aws_session_token = get_aws_sts_assume_role_credentials()
"""
"""
def generate_voices() -> None:
    raise NotImplementedError
    for key in keys:
        set_api_key(key)
        required_script = "Good evening, my name is Serenity, and I'll do my best to help you today. Why don't you introduce yourself."
        voice_design = VoiceDesign(name=f"{key}-female-british", text=required_script, gender=Gender.female, age=Age.young, accent=Accent.british, accent_strength=1.3, generated_voice_id=None, audio=None)
        voice_design.generate()
        print(f'        "{key}": "{voice_design.generated_voice_id}",')
"""
