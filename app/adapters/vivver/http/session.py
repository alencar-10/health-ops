import requests

BASE = "https://guaraciama-mg-tst.vivver.com"


def create_session_from_cookies(cookies):

    session = requests.Session()

    for c in cookies:

        session.cookies.set(
            name=c["name"],
            value=c["value"],
            domain="guaraciama-mg-tst.vivver.com",
            path="/"
        )

    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": BASE,
        "Referer": BASE + "/desktop",
        "Accept": "*/*"
    })

    return session