"""Test College Football Sensor"""
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.college_football.const import DOMAIN
from tests.const import CONFIG_DATA


async def test_sensor(hass):

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="College_Football",
        data=CONFIG_DATA,
    )

    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert "college_football" in hass.config.components

    
