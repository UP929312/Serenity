import requests
from datetime import datetime, timedelta

today = datetime.now().date()
before = today - timedelta(days=99)


def test_open_ai_cost() -> dict[str, float]:
    """
    Fails if we have spent more than £0.15 in one day
    """
    with open("keys/openai_key.txt", "r", encoding="utf-8") as file:
        openai_api_key = file.read().strip()

    URL = f"https://api.openai.com/dashboard/billing/usage?start_date={before}&end_date={today}"
    request = requests.get(URL, headers={"Authorization": f"Bearer {openai_api_key}"}).json()

    costs_days = [x for x in request["daily_costs"] if any(y for y in x["line_items"] if y["cost"] != 0.0)]
    cost_points = {}
    for cost_day in costs_days:
        timestamp = cost_day["timestamp"]
        for cost_point in cost_day["line_items"]:
            if cost_point["cost"] != 0.0:
                cost_points[timestamp] = cost_point

    # cost_points = {1683849600.0: {'name': 'Chat models', 'cost': 0.8586}, 1683936000.0: {'name': 'Chat models', 'cost': 7.5728}, 1684108800.0: {'name': 'Chat models', 'cost': 0.3294}, 1684195200.0: {'name': 'Instruct models', 'cost': 10.162}, 1684281600.0: {'name': 'Instruct models', 'cost': 0.202}, 1684454400.0: {'name': 'Instruct models', 'cost': 0.434}, 1684886400.0: {'name': 'Instruct models', 'cost': 0.376}, 1684972800.0: {'name': 'Instruct models', 'cost': 11.346}}
    datetime_instead: dict[str, float] = {str(datetime.fromtimestamp(x).date()): y["cost"] for x, y in cost_points.items()}
    for date, cost in datetime_instead.items():
        assert cost < 15, f"Spent £{cost} on {date}, which is too much"
    return datetime_instead


def test_deepgram_remaining_credits() -> float:
    """
    Tests to see if we've got over $180 worth of credits left
    """
    with open("keys/deepgram_key.txt", "r", encoding="utf-8") as file:
        DEEPGRAM_API_KEY = file.read().strip()

    DEEPGRAM_PROJECT_ID = "64152c31-f748-4ac9-82a5-2106f12d1091"
    url = f"https://api.deepgram.com/v1/projects/{DEEPGRAM_PROJECT_ID}/balances"

    headers = {"accept": "application/json", "Authorization": f"Token {DEEPGRAM_API_KEY}"}
    response = requests.get(url, headers=headers).json()
    amount_left = response["balances"][0]["amount"]
    assert amount_left > 180, f"Deepgram only has {amount_left} credits left"
    return amount_left


def test_elevenlabs_remaining_characters() -> list[int]:
    """
    Tests to make sure we've got at least half our capacity left (on average)
    """
    from monitor_elevenlabs import monitor_elevenlabs_keys
    
    key_dict = monitor_elevenlabs_keys(False).values()
    half = len(key_dict) * 5000
    current_remaining = sum(key_dict)
    assert current_remaining > half, f"Eleven Labs only has {current_remaining}/{half*2} characters left"
    return list(key_dict)
