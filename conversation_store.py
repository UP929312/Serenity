import json

def store_conversation_row(username: str, message: str, user: str, tone: str|None) -> None:
    #print("Storing conversation row")
    with open("file_store.json", "r") as file:
        data = json.load(file)
    data[username].append({"message": message, "user": user, "tone": tone})
    with open("file_store.json", "w") as file:
        json.dump(data, file, indent=4)

def load_conversation_history(username: str) -> list[dict]:
    #print("Loading conversation history")
    with open("file_store.json", "r") as file:
        data = json.load(file)
    return data[username]