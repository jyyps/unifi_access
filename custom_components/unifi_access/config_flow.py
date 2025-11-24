import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_HOST, CONF_TOKEN
from .api import UniFiAccessAPI

class UniFiAccessConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for UniFi Access."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step from the user."""
        errors = {}

        if user_input is not None:
            # Validate host and token
            host = user_input[CONF_HOST]
            token = user_input[CONF_TOKEN]
            api = UniFiAccessAPI(host, token, self.hass)

            try:
                devices = await api.get_devices()
                if devices is None:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(title=f"UniFi Access ({host})", data=user_input)
            except Exception:
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=""): str,
            vol.Required(CONF_TOKEN, default=""): str
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
