from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors."""
    data = hass.data[DOMAIN][entry.entry_id]["api"]
    devices = await data.get("devices")
    entities = []

    for device in devices.get("doors", []):
        entities.append(UniFiDoorSensor(device, hass))

    async_add_entities(entities)

class UniFiDoorSensor(BinarySensorEntity):
    def __init__(self, device, hass):
        self._device = device
        self._hass = hass
        self._attr_name = device["name"]
        self._attr_is_on = device.get("state") == "open"

        hass.bus.async_listen("unifi_access_event", self._handle_event)

    def _handle_event(self, event):
        if event.get("device_id") == self._device["id"]:
            if event["type"] in ["door_opened", "door_closed"]:
                self._attr_is_on = event["type"] == "door_opened"
                self.schedule_update_ha_state()

    @property
    def is_on(self):
        return self._attr_is_on
