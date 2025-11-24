from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .api import UniFiAccessAPI
from .websocket import UniFiAccessWebsocket

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass, entry):
    host = entry.data["host"]
    token = entry.data.get("token")
    username = entry.data.get("username")
    password = entry.data.get("password")

    api = UniFiAccessAPI(host, token, username, password, hass)
    ws = UniFiAccessWebsocket(api, hass)
    hass.loop.create_task(ws.connect())

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"api": api, "ws": ws}

    for platform in ["binary_sensor", "lock", "sensor"]:
        hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, platform))

    return True

async def async_unload_entry(hass, entry):
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
