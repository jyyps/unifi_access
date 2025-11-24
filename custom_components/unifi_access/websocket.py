import aiohttp
import asyncio
import json

class UniFiAccessWebsocket:
    def __init__(self, api):
        self.api = api
        self.ws = None
        self.running = True

    async def connect(self):
        url = f"wss://{self.api.host}/ws/updates"
        headers = {"Authorization": f"Bearer {self.api.token}"}

        while self.running:
            try:
                async with self.api.session.ws_connect(url, headers=headers, ssl=False) as ws:
                    self.ws = ws
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            event = json.loads(msg.data)
                            self.api.hass.bus.async_fire("unifi_access_event", event)
            except Exception:
                await asyncio.sleep(5)

    async def close(self):
        self.running = False
        if self.ws:
            await self.ws.close()
