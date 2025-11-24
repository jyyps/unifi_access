import aiohttp

class UniFiAccessAPI:
    def __init__(self, host, token=None, username=None, password=None, hass=None):
        self.host = host
        self.token = token
        self.username = username
        self.password = password
        self.hass = hass
        self.session = aiohttp.ClientSession()

    async def get_headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return None

    async def get_devices(self):
        url = f"https://{self.host}/api/devices"
        headers = await self.get_headers()
        auth = None
        if not headers and self.username and self.password:
            auth = aiohttp.BasicAuth(self.username, self.password)

        try:
            async with self.session.get(url, headers=headers, auth=auth, ssl=False) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception:
            return None
