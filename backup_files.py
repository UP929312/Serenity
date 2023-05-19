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

# self.last_agent_response = ""
        # self.last_human_response = ""


"""
async def send(_ws, audio_data) -> Literal[True]:
    while True:
        try:
            data = base64.b64encode(audio_data).decode("utf-8")
            # print(f"{data=}")
            json_data = json.dumps({"audio_data": str(data)})
            await _ws.send(json_data)
        except websockets.exceptions.ConnectionClosedError as e:  # type: ignore
            print(e)
            assert e.code == 4008
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error"
        await asyncio.sleep(0.01)
    return True


async def receive(_ws) -> None:
    while True:
        try:
            result_str = await _ws.recv()
            print(json.loads(result_str)["text"])
        except websockets.exceptions.ConnectionClosedError as e:  # type: ignore
            print(e)
            assert e.code == 4008
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error"
"""