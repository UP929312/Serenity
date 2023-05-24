from elevenlabs import set_api_key
from elevenlabs import  User

with open("keys/eleven_labs_keys.txt", "r") as file:
    keys = file.read().strip().split("\n")

def monitor_elevenlabs_keys(redact_keys: bool=True) -> None:
    for key in keys:
        #print(i, key)
        set_api_key(key)
        user = User.from_api()
        print(f"{key if not redact_keys else '[REDACTED]'}'s remaining balance: {10000-user.subscription.character_count}")

if __name__ == "__main__":
    monitor_elevenlabs_keys()