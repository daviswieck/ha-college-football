import logging
import uuid

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify
from . import CollegeFootballDataUpdateCoordinator

from .const import (
    ATTRIBUTION,
    CONF_TIMEOUT,
    CONF_TEAM_ID,
    COORDINATOR,
    DEFAULT_ICON,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_TEAM_ID): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Configuration from yaml"""
    if DOMAIN not in hass.data.keys():
        hass.data.setdefault(DOMAIN, {})
        config.entry_id = slugify(f"{config.get(CONF_TEAM_ID)}")
        config.data = config
    else:
        config.entry_id = slugify(f"{config.get(CONF_TEAM_ID)}")
        config.data = config

    # Setup the data coordinator
    coordinator = CollegeFootballDataUpdateCoordinator(
        hass,
        config,
        config[CONF_TIMEOUT],
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN][config.entry_id] = {
        COORDINATOR: coordinator,
    }
    async_add_entities([CollegeFootballScoresSensor(hass, config)], True)

async def async_setup_entry(hass, entry, async_add_entities):
    """Setup the sensor platform."""
    async_add_entities([CollegeFootballScoresSensor(hass, entry)], True)

class CollegeFootballScoresSensor(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(hass.data[DOMAIN][entry.entry_id][COORDINATOR])
        self._config = entry
        self._name = entry.data[CONF_NAME]
        self._icon = DEFAULT_ICON
        self._state = "PRE"
        self._date = None
        self._kickoff_in = None
        self._quarter = None
        self._clock = None
        self._venue = None
        self._location = None
        self._tv_network = None
        self._odds = None
        self._overunder = None
        self._possession = None
        self._last_play = None
        self._down_distance_text = None
        self._team_abbr = None
        self._team_id = None
        self._team_name = None
        self._team_record = None
        self._team_homeaway = None
        self._team_logo = None
        self._team_colors = None
        self._team_score = None
        self._team_rank = None 
        self._team_win_probability = None
        self._team_timeouts = None
        self._opponent_abbr = None
        self._opponent_id = None
        self._opponent_name = None
        self._opponent_record = None
        self._opponent_homeaway = None
        self._opponent_logo = None
        self._opponent_colors = None
        self._opponent_score = None
        self._opponent_rank = None
        self._opponent_win_probability = None
        self._opponent_timeouts = None
        self._last_update = None
        self._team_id = entry.data[CONF_TEAM_ID]
        self.coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    @property
    def unique_id(self):
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return f"{slugify(self._name)}_{self._config.entry_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        elif "state" in self.coordinator.data.keys():
            return self.coordinator.data["state"]
        else:
            return None

    @property
    def extra_state_attributes(self):
        """Return the state message."""
        attrs = {}

        if self.coordinator.data is None:
            return attrs

        attrs[ATTR_ATTRIBUTION] = ATTRIBUTION
        attrs["date"] = self.coordinator.data.get("date")
        attrs["kickoff_in"] = self.coordinator.data.get("kickoff_in")
        attrs["quarter"] = self.coordinator.data.get("quarter")
        attrs["clock"] = self.coordinator.data.get("clock")
        attrs["venue"] = self.coordinator.data.get("venue")
        attrs["location"] = self.coordinator.data.get("location")
        attrs["tv_network"] = self.coordinator.data.get("tv_network")
        attrs["odds"] = self.coordinator.data.get("odds")
        attrs["overunder"] = self.coordinator.data.get("overunder")
        attrs["possession"] = self.coordinator.data.get("possession")
        attrs["last_play"] = self.coordinator.data.get("last_play")
        attrs["down_distance_text"] = self.coordinator.data.get("down_distance_text")
        attrs["team_abbr"] = self.coordinator.data.get("team_abbr")
        attrs["team_id"] = self.coordinator.data.get("team_id")
        attrs["team_name"] = self.coordinator.data.get("team_name")
        attrs["team_record"] = self.coordinator.data.get("team_record")
        attrs["team_homeaway"] = self.coordinator.data.get("team_homeaway")
        attrs["team_logo"] = self.coordinator.data.get("team_logo")
        attrs["team_colors"] = self.coordinator.data.get("team_colors")
        attrs["team_colors_rgb"] = self.team_colors(self.coordinator.data.get("team_colors"))
        attrs["team_score"] = self.coordinator.data.get("team_score")
        attrs["team_rank"] = self.coordinator.data.get("team_rank")
        attrs["team_win_probability"] = self.coordinator.data.get("team_win_probability")
        attrs["team_timeouts"] = self.coordinator.data.get("team_timeouts")
        attrs["opponent_abbr"] = self.coordinator.data.get("opponent_abbr")
        attrs["opponent_id"] = self.coordinator.data.get("opponent_id")
        attrs["opponent_name"] = self.coordinator.data.get("opponent_name")
        attrs["opponent_record"] = self.coordinator.data.get("opponent_record")
        attrs["opponent_homeaway"] = self.coordinator.data.get("opponent_homeaway")
        attrs["opponent_logo"] = self.coordinator.data.get("opponent_logo")
        attrs["opponent_colors"] = self.coordinator.data.get("opponent_colors")
        attrs["opponent_colors_rgb"] = self.team_colors(self.coordinator.data.get("opponent_colors"))
        attrs["opponent_score"] = self.coordinator.data.get("opponent_score")
        attrs["opponent_rank"] = self.coordinator.data.get("opponent_rank")
        attrs["opponent_win_probability"] = self.coordinator.data.get("opponent_win_probability")
        attrs["opponent_timeouts"] = self.coordinator.data.get("opponent_timeouts")
        attrs["last_update"] = self.coordinator.data.get("last_update")

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    def team_colors(self, colors) -> tuple:
        if colors is None:
            return None
        color_list = []
        _LOGGER.debug("Colors: %s", colors[0])
        color_list.append(list(self.hex_to_rgb(colors[0])))
        color_list.append(list(self.hex_to_rgb(colors[1])))
        return color_list

    def hex_to_rgb(self, hexa) -> tuple:
        hexa = hexa.lstrip("#")
        return tuple(int(hexa[i: i + 2], 16) for i in (0, 2, 4))
