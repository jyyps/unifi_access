import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_TOKEN, CONF_USERNAME, CONF_PASSWORD
from .api import UniFiAccessAPI

class UniFiAccessConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for UniFi Access."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Initial step asking for host and auth method."""
        errors = {}

        if user_input is not None:
            auth_type = user_input.get("auth_type")
            self.hass.data["auth_type"] = auth_type
            return await self.async_step_credentials()

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=""): str,
            vol.Required("auth_type", default="token"): vol.In(["token", "username_password"])
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    async def async_step_credentials(self, user_input=None):
        """Ask for either API token or username/password based on selection."""
        errors = {}
        auth_type = self.hass.data.get("auth_type", "token")

        if user_input is not None:
            host = user_input[CONF_HOST]
            token = user_input.get(CONF_TOKEN)
            username = user_input.get(CONF_USERNAME)
            password = user_input.get(CONF_PASSWORD)

            api = UniFiAccessAPI(host, token, username, password, self.hass)

            try:
                devices = await api.get_devices()
                if devices is None:
                    errors["base"] = "cannot_connect"
                else:
                    return self.async_create_entry(
                        title=f"UniFi Access ({host})", data=user_input
                    )
            except Exception:
                errors["base"] = "cannot_connect"

        if auth_type == "token":
            data_schema = vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_TOKEN): str
            })
        else:
            data_schema = vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str
            })

        return self.async_show_form(
            step_id="credentials",
            data_schema=data_schema,
            errors=errors
        )
