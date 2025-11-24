import aiohttp
import async_timeout

class UniFiAccessAPI:
    def __init__(self, host, token, hass):
        self.host = host
        self.token = token
        self.hass = hass
        self.session = aiohttp.ClientSession()

    async def get(self, path):
        headers = {"Authorization": f"Bearer {self.token}"}
        async with async_timeout.timeout(10):
            async with self.session.get(f"https://{self.host}/api/access/v1/{path}", headers=headers, ssl=False) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def close(self):
        await self.session.close()
