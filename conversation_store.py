import json
from datetime import datetime
from typing import Any, TypedDict, Literal

# ==================================

class ConversationRow(TypedDict):
    username: str
    message: str
    user: Literal["user", "agent"]
    dt: datetime
    tone: str | None
    facial_emoji: str | None


class DatetimeEncoder(json.JSONEncoder):
    """A custom encoder to convert datetime objects to strings"""
    def default(self, o: Any) -> Any:
        try:
            return super().default(o)
        except TypeError:
            return str(o)


class DatetimeDecoder(json.JSONDecoder):
    """When reading a json file, will convert any key with the name in the set to a datetime object."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: Any) -> dict[Any, Any]:
        ret = {}
        for key, value in obj.items():
            ret[key] = datetime.fromisoformat(value) if key in {"timestamp", "expires", "dt", "datetime"} else value
        return ret


# ==================================


def store_conversation_row(username: str, message: str, user: str, tone: str | None, facial_emotion: str | None) -> None:  # fmt: ignore
    """Stores a single monologue in the database, with which profile said it, what it had, the tone and facial expression."""
    # print("Storing conversation row")
    with open("assets/files/file_store.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    data[username].append(
        {
            "username": username,
            "message": message,
            "user": user,
            "dt": str(datetime.now()),
            "tone": tone,
            "facial_emoji": facial_emotion,
        }
    )
    with open("assets/files/file_store.json", "w") as file:
        json.dump(data, file, cls=DatetimeEncoder, indent=4)


def load_conversation_history(username: str) -> list[ConversationRow]:
    """Loads a list of dictionaries containing the conversation history for a given user. Sorted by datetime."""
    # print("Loading conversation history")
    with open("assets/files/file_store.json", "r", encoding="utf-8") as file:
        data: dict[str, list[ConversationRow]] = json.load(file, cls=DatetimeDecoder)
    return sorted(data[username], key=lambda x: x["dt"])
