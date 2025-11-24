import logging
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .api import UniFiAccessAPI
from .websocket import UniFiAccessWebsocket

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration via configuration.yaml (optional)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up UniFi Access from a config entry."""
    host = entry.data["host"]
    token = entry.data["token"]

    # Initialize API
    api = UniFiAccessAPI(host, token, hass)

    # Connect WebSocket
    ws = UniFiAccessWebsocket(api, hass)
    hass.loop.create_task(ws.connect())

    # Save objects to hass.data
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "api": api,
        "ws": ws
    }

    # Set up platforms
    for platform in ["binary_sensor", "lock", "sensor"]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
