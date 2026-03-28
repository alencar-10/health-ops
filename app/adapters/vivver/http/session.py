import requests


def create_session_from_cookies(cookies: list) -> requests.Session:
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    return session