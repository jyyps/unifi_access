from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensors from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    devices = await api.get_devices()
    sensors = []

    for device in devices:
        if "battery" in device:
            sensors.append(UniFiBatterySensor(device))

    async_add_entities(sensors, True)

class UniFiBatterySensor(SensorEntity):
    """Battery sensor for UniFi Access devices."""

    def __init__(self, device):
        self.device = device
        self._attr_name = f"{device.get('name', 'UniFi Device')} Battery"
        self._attr_native_value = device.get("battery", 100)

    @property
    def native_value(self):
        return self._attr_native_value

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.get("id"))},
            "name": self.device.get("name", "UniFi Device"),
            "model": self.device.get("model", "UniFi Sensor"),
        }
