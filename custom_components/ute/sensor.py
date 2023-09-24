import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorDeviceClass, SensorEntity
from homeassistant.const import CONF_EMAIL, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from ute_wrapper.ute import UTEClient

_LOGGER = logging.getLogger(__name__)
# Time between updating data from UTE
SCAN_INTERVAL = timedelta(minutes=2)

CONF_PHONE_NUMBER = "phone_number"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PHONE_NUMBER): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    email = config[CONF_EMAIL]
    phone_number = config[CONF_PHONE_NUMBER]

    client = UTEClient(email, phone_number)
    add_entities([UTESensor(client)], True)


class UTESensor(SensorEntity):
    """Representation of a UTE sensor."""

    _attr_name = "UTE Uruguay Client"
    _attr_icon = "lightning-bolt"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.ENERGY

    def __init__(self, ute: UTEClient):
        super().__init__()
        self.ute = ute
        self._state = None
        self._available = True
        self._name = "Current energy usage"

    def update(self):
        ute_data = self.ute.get_current_usage_info()
        self._attr_native_value = ute_data["data"]["power_in_watts"]
