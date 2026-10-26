import aiohttp
import async_timeout

class IFloApiClient:
    def __init__(self, token: str, session: aiohttp.ClientSession) -> None:
        self._token = token
        self._session = session

    async def async_get_data(self):
        url = "https://backend.iflo.com/api/v1/locations"
        headers = {
            "x-access-token": self._token,
            "Accept": "application/json"
        }
        async with async_timeout.timeout(10):
            response = await self._session.get(url, headers=headers)
            response.raise_for_status()
            return await response.json()
