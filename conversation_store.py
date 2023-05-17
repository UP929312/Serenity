import json
from datetime import datetime
from typing import Any

# ==================================

class DatetimeEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        try:
            return super().default(o)
        except TypeError:
            return str(o)

class DatetimeDecoder(json.JSONDecoder):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: Any) -> dict[Any, Any]:
        ret = {}
        for key, value in obj.items():
            ret[key] = datetime.fromisoformat(value) if key in {'timestamp', 'expires'} else value
        return ret

# ==================================

def store_conversation_row(username: str, message: str, user: str, dt: datetime, tone: str|None) -> None:
    #print("Storing conversation row")
    with open("file_store.json", "r") as file:
        data = json.load(file)
    data[username].append({"message": message, "user": user, "dt": str(dt), "tone": tone})
    with open("file_store.json", "w") as file:
        json.dump(data, file, cls=DatetimeEncoder, indent=4)

def load_conversation_history(username: str) -> list[dict]:
    #print("Loading conversation history")
    with open("file_store.json", "r") as file:
        data = json.load(file, cls=DatetimeDecoder)
    return data[username]