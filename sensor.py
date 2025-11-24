from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]["api"]
    devices = await data.get("devices")
    entities = []

    for sensor in devices.get("sensors", []):
        entities.append(UniFiSensor(sensor, hass))

    async_add_entities(entities)

class UniFiSensor(SensorEntity):
    def __init__(self, sensor, hass):
        self._sensor = sensor
        self._hass = hass
        self._attr_name = sensor["name"]
        self._attr_native_value = sensor.get("value")

        hass.bus.async_listen("unifi_access_event", self._handle_event)

    def _handle_event(self, event):
        if event.get("device_id") == self._sensor["id"]:
            self._attr_native_value = event.get("value", self._attr_native_value)
            self.schedule_update_ha_state()
