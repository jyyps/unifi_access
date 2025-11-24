from homeassistant.components.lock import LockEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]["api"]
    devices = await data.get("devices")
    entities = []

    for lock in devices.get("locks", []):
        entities.append(UniFiLock(lock, hass))

    async_add_entities(entities)

class UniFiLock(LockEntity):
    def __init__(self, lock, hass):
        self._lock = lock
        self._hass = hass
        self._attr_name = lock["name"]
        self._attr_is_locked = lock.get("state") == "locked"

        hass.bus.async_listen("unifi_access_event", self._handle_event)

    def _handle_event(self, event):
        if event.get("device_id") == self._lock["id"]:
            if event["type"] in ["lock_engaged", "lock_released"]:
                self._attr_is_locked = event["type"] == "lock_engaged"
                self.schedule_update_ha_state()

    async def async_lock(self, **kwargs):
        # implement lock API call here
        pass

    async def async_unlock(self, **kwargs):
        # implement unlock API call here
        pass
