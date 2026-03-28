import requests


def create_session_from_cookies(cookies: list) -> requests.Session:
    session = requests.Session()

    for cookie in cookies:
        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path"),
        )

    return session