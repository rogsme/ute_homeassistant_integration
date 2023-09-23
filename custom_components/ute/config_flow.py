import re
import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_PHONE_NUMBER = "phone_number"
CONF_UTE_DEVICE_ID = "ute_device_id"
CONF_UTE_AVERAGE_COST_PER_KWH = "average_cost_per_kwh"

schema = {
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PHONE_NUMBER): cv.string,
    vol.Optional(CONF_UTE_DEVICE_ID): cv.string,
    vol.Optional(CONF_UTE_AVERAGE_COST_PER_KWH): cv.string,
}

AUTH_SCHEMA = vol.Schema(schema)


def validate_email(email: str) -> None:
    """
    Validates a email address

    Args:
        email: The email address to validate.

    Raises:
        ValueError: If the email address is invalid.
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError


async def validate_uyu_phone_number(phone_number: str) -> None:
    """
    Validates a Uruguayan phone number

    Args:
        phone_number: The phone number to validate.

    Raises:
        ValueError: If the phone number is invalid.
    """
    if not phone_number.startswith("598"):
        raise ValueError

    if not re.match(r"^[0-9]{11}$", phone_number):
        raise ValueError


class UTEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """
    UTE Custom config flow.

    Args:
        config_entries: The config entries.
        domain: The domain.

    Returns:
        The config flow.
    """

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                validate_email(user_input[CONF_EMAIL])
                validate_uyu_phone_number(user_input[CONF_PHONE_NUMBER])
            except ValueError:
                errors["base"] = "auth"
            if not errors:
                # Input is valid, set data.
                self.data = user_input

        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )
