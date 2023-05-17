#import openai
#openai.api_key

"""
messages = [{"role": "system", "content":
             "You are a virtual therapist. You will do your best to guide and advise the user on how to progress. "
             "You will ask questions about the user, especially when you're unsure of anything."}]

while True:
    message = input("User: ")
    if message:
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    convert_text_to_speech(reply, play_message=True)
    messages.append({"role": "assistant", "content": reply})
"""

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