# UTE (Administración Nacional de Usinas y Trasmisiones Eléctricas) for Home Assistant 🇺🇾
![License](https://img.shields.io/github/license/rogsme/ute_homeassistant_integration)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/rogsme/ute_homeassistant_integration)

<p align="center">
  <img src="https://github.com/rogsme/ute_homeassistant_integration/blob/master/icon.png?raw=true" alt="UTE"/>
</p>

# What is UTE?

From Wikipedia
> The National Administration of Power Plants and Electrical Transmissions (Spanish: Administración Nacional de Usinas y Trasmisiones Eléctricas), better known as UTE, is Uruguay's government-owned power company. It was established in 1912, following approval of Law 4273 establishing it as a monopoly.

This is an integration to get UTE power information in HomeAssistant.

# Installation via HACS

Have [HACS](https://hacs.xyz/) installed, this will allow you to update easily.

* Add `https://github.com/rogsme/ute_homeassistant_integration` as a custom repository of type Integration in HACS.
* Click Install on the `UTE` integration.
* Restart the Home Assistant.

## Configuration

Add the following to your `configuration.yaml`:
```yaml
sensor:
  - platform: ute
    email: your@email.com
    phone_number: 598123456
    power_factor: 0.5 # Optional, must be a float between 0 and 1
  - platform: integration
    source: sensor.ute_current_power_usage
    name: Home energy spent
    unit_prefix: k
    round: 2
    method: left
```

And restart Home Assistant.

# Contributing

Contributions are welcome! If you find a bug or have a suggestion, please create an issue or submit Pull Request on [Github](https://github.com/rogsme/ute_homeassistant_integration).

# License

This project is licensed under the GNU General Public License, version 3.0. For more details, see [LICENSE](LICENSE).

---

*This project is not affiliated with UTE (Administración Nacional de Usinas y Trasmisiones Eléctricas) or its affiliates.*
