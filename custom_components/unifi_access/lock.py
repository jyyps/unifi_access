from homeassistant.components.lock import LockEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up locks from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    devices = await api.get_devices()
    locks = []

    for device in devices:
        if device.get("type") == "lock":
            locks.append(UniFiDoorLock(device))

    async_add_entities(locks, True)

class UniFiDoorLock(LockEntity):
    """Representation of a UniFi Access lock."""

    def __init__(self, device):
        self.device = device
        self._attr_name = device.get("name", "UniFi Lock")
        self._locked = device.get("locked", True)

    @property
    def is_locked(self):
        return self._locked

    async def async_lock(self, **kwargs):
        # Call API to lock the door
        self._locked = True

    async def async_unlock(self, **kwargs):
        # Call API to unlock the door
        self._locked = False

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.get("id"))},
            "name": self._attr_name,
            "model": self.device.get("model", "UniFi Lock"),
        }
