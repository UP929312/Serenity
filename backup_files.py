import openai
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