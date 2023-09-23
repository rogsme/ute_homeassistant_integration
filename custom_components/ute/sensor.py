from datetime import timedelta
import logging
from typing import Callable, Optional

from ute_wrapper.ute import UTEClient
from homeassistant import config_entries, core
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_EMAIL, CONF_PHONE_NUMBER, CONF_UTE_DEVICE_ID, CONF_UTE_AVERAGE_COST_PER_KWH
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from .const import DOMAIN
from .config_flow import schema

_LOGGER = logging.getLogger(__name__)
# Time between updating data from UTE
SCAN_INTERVAL = timedelta(minutes=2)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(schema)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    ute = UTEClient(
        config[CONF_EMAIL],
        config[CONF_PHONE_NUMBER],
        config[CONF_UTE_DEVICE_ID],
        config[CONF_UTE_AVERAGE_COST_PER_KWH],
    )
    sensor = UTESensor(ute)
    async_add_entities(sensor, update_before_add=True)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    ute = UTEClient(
        config[CONF_EMAIL],
        config[CONF_PHONE_NUMBER],
        config[CONF_UTE_DEVICE_ID],
        config[CONF_UTE_AVERAGE_COST_PER_KWH],
    )
    sensor = UTESensor(ute)
    async_add_entities(sensor, update_before_add=True)


class UTESensor(Entity):
    """Representation of a UTE sensor."""

    def __init__(self, ute: UTEClient):
        super().__init__()
        self.ute = ute
        self._state = None
        self._available = True
        self._name = "Current energy usage"

    async def async_update(self):
        try:
            ute_data = await self.ute.get_current_usage_info()
            self._state = ute_data["data"]["power_in_watts"]
        except ():
            pass
