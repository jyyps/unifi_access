import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_TOKEN
from .api import UniFiAccessAPI

class UniFiAccessConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            token = user_input[CONF_TOKEN]
            api = UniFiAccessAPI(host, token, self.hass)

            try:
                await api.get("devices")
                await api.close()
            except Exception:
                errors["base"] = "cannot_connect"

            if not errors:
                return self.async_create_entry(title=f"UniFi Access ({host})", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_TOKEN): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
