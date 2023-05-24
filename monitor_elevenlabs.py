from elevenlabs import set_api_key
from elevenlabs import User

with open("keys/eleven_labs_keys.txt", "r") as file:
    keys = file.read().strip().split("\n")


def monitor_elevenlabs_keys(redact_keys: bool = True) -> dict[str, int]:
    dictionary = {}
    for i, key in enumerate(keys, 1):
        # print(i, key)
        set_api_key(key)
        user = User.from_api()
        dictionary[key if not redact_keys else f"Key {i}"] = 10000 - user.subscription.character_count
    return dictionary


# Creation dates: 24/05/2023, roughly 9am, datetime(2023, 5, 24, 9, 0, 0, 0)

if __name__ == "__main__":
    for key, remaining_chars in monitor_elevenlabs_keys(False).items():
        print(f"{key}'s remaining balance: {remaining_chars}")