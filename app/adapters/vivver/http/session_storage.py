import json

def save_cookies(cookies, path="cookies.json"):
    with open(path, "w") as f:
        json.dump(cookies, f)


def load_cookies(path="cookies.json"):
    with open(path, "r") as f:
        return json.load(f)