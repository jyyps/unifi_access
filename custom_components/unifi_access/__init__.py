from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .api import UniFiAccessAPI
from .websocket import UniFiAccessWebsocket

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    api = UniFiAccessAPI(entry.data["host"], entry.data["token"], hass)
    ws = UniFiAccessWebsocket(api)
    await ws.connect()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"api": api, "ws": ws}

    hass.config_entries.async_setup_platforms(entry, ["binary_sensor", "lock", "sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    data = hass.data[DOMAIN][entry.entry_id]
    await data["ws"].close()
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
