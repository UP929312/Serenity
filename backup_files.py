# import openai
# openai.api_key

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

# Handle agent avatar
# self.agent_avatar.animate(self.last_agent_response_sentiment)  # Should be threaded, but currently does nothing

"""
class STTWebhookHandler:
    def __init__(self, on_receive: Callable[[str], None]) -> None:
        self.on_receive = on_receive

        URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
        self.webhook = websockets.connect(URL, extra_headers=(("Authorization", auth_key),), ping_interval=5, ping_timeout=20)  # type: ignore[attr-defined]
        self.last_send = datetime.now()

        thread = threading.Thread(target=self.keep_alive)
        thread.start()
        # #self.webhook.close()  # Somewhere, we need to close the websocket, or we can just let it die?

    async def keep_alive(self) -> None:
        if self.last_send + timedelta(seconds=55) < datetime.now():  # If the last send was more than 55 seconds ago
            asyncio.run(self.send(b""))

    async def send(self, audio_data: bytes) -> None:
        data = base64.b64encode(audio_data).decode("utf-8")
        json_data = json.dumps({"audio_data": str(data)})
        await self.webhook.send(json_data)
        self.last_send = datetime.now()

    async def receive(self) -> None:
        result_str = await self.webhook.recv()
        string = json.loads(result_str)["text"]
        self.on_receive(string)
"""

"""
    def on_error(self, _, error) -> None:
        if isinstance(error, Exception):
            print("Error: ", error)
        else:
            error_message = json.loads(error)
            print(f"{error_message=}")

"""