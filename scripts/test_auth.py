import asyncio
from app.adapters.vivver.http.auth import get_authenticated_session
from app.adapters.vivver.http.auth import (
    get_authenticated_session,
    get_session_from_disk,
    is_session_valid,
)


async def main():
    session = get_session_from_disk()

    if not session or not is_session_valid(session):
        print("🔄 Sessão inválida, refazendo login...")
        session = await get_authenticated_session()

    print("Session criada:", session)
    print("Cookies:", session.cookies.get_dict())

asyncio.run(main()) 