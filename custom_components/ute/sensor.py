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
SCAN_INTERVAL = timedelta(minutes=3)

CONF_PHONE_NUMBER = "phone_number"
CONF_POWER_FACTOR = "power_factor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PHONE_NUMBER): cv.string,
        vol.Optional(CONF_POWER_FACTOR): cv.positive_float,
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
    power_factor = None

    if CONF_POWER_FACTOR in config:
        power_factor = config[CONF_POWER_FACTOR]

    try:
        client = UTEClient(email, phone_number, power_factor=power_factor)
    except Exception:
        _LOGGER.error("Could not connect to UTE")
        return

    add_entities([UTESensor(client)], True)


class UTESensor(SensorEntity):
    """Representation of a UTE sensor."""

    _attr_name = "UTE Current power usage"
    _attr_icon = "lightning-bolt"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER

    def __init__(self, client: UTEClient):
        super().__init__()
        self.client = client
        self._name = "Current energy usage"
        self._attr_extra_state_attributes = {}

    def update(self):
        ute_data = self.client.get_current_usage_info()["data"]
        self._attr_native_value = ute_data["power_in_watts"]
        self._attr_extra_state_attributes["using_power_factor"] = ute_data["using_power_factor"]
        self._attr_extra_state_attributes["last_query_date"] = ute_data["lastQueryDate"]
        self._attr_extra_state_attributes["last_response_date"] = ute_data["lastResponseDate"]
        self._attr_extra_state_attributes["energy_status"] = ute_data["statusText"]

        readings = ute_data["readings"]

        for reading in readings:
            reading_type = reading["tipoLecturaMGMI"]
            if reading_type != "RELAY_ON":
                self._attr_extra_state_attributes[reading_type] = reading["valor"]
                self._attr_extra_state_attributes["reading_date"] = reading["fechaHora"]
