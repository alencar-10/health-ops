import asyncio
from app.adapters.vivver.http.auth import get_authenticated_session

async def main():
    session = await get_authenticated_session()
    print("Session criada:", session)
    print("Cookies:", session.cookies.get_dict())

asyncio.run(main())