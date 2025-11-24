from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    devices = await api.get_devices()
    sensors = []

    for device in devices:
        if device.get("type") == "door":
            sensors.append(UniFiDoorSensor(device))

    async_add_entities(sensors, True)

class UniFiDoorSensor(BinarySensorEntity):
    """Representation of a UniFi Access door sensor."""

    def __init__(self, device):
        self.device = device
        self._attr_name = device.get("name", "UniFi Door")
        self._attr_is_on = device.get("state") == "open"

    @property
    def is_on(self):
        """Return True if the door is open."""
        return self._attr_is_on

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.get("id"))},
            "name": self._attr_name,
            "model": self.device.get("model", "UniFi Door"),
        }
