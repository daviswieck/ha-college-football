"""Adds config flow for College Football."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    API_ENDPOINT,
    CONF_TIMEOUT,
    CONF_TEAM_ID,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
    USER_AGENT,
)

JSON_FEATURES = "features"
JSON_PROPERTIES = "properties"
JSON_ID = "id"

_LOGGER = logging.getLogger(__name__)


def _get_schema(    
    hass: HomeAssistant,
    user_input: Optional[Dict[str, Any]],
    default_dict: Dict[str, Any],
    entry_id: str = None
) -> vol.Schema:
    """Gets a schema using the default_dict as a backup."""
    if user_input is None:
        user_input = {}

    def _get_default(key: str, fallback_default: Any = None) -> None:
        """Gets default value for key."""
        return user_input.get(key, default_dict.get(key, fallback_default))

    return vol.Schema(
        {
            vol.Required(CONF_TEAM_ID, default=_get_default(CONF_TEAM_ID,_get_team_list())): str,
            vol.Optional(CONF_NAME, default=_get_default(CONF_NAME, DEFAULT_NAME)): str,
            vol.Optional(CONF_TIMEOUT, default=_get_default(CONF_TIMEOUT, DEFAULT_TIMEOUT)): int,
        }
    )


def _get_team_list() -> list:
    """Return list of team acronyms"""

    team_list = [
#### FBS SCHOOLS ####
        ## BIG 12 ##
        "TTU",
        "TEX",
        "WVU",
        "TCU",
        "OKST",
        "KSU",
        "ISU",
        "OU",
        "BAY",
        "KU",
        ## ACC ##
        "BC",
        "CLEM",
        "DUKE",
        "FSU",   
        "GT",
        "LOU",
        "MIA",
        "UNC",
        "NCST",
        "PITT",
        "SYR",
        "UVA",
        "VT",
        "WAKE",
        "ND",
        ## BIG 10 ##
        "ILL",
        "IU",
        "IOWA",
        "MD",
        "MICH",
        "MSU",
        "MINN",
        "NEB",
        "NU",
        "OSU",
        "PSU",
        "PUR",
        "RUTG",
        "WISC",
        ## PAC 12 ##
        'ARIZ',
        'ASU',
        'CAL',
        'UCLA',
        'COLO',
        'ORE',
        'ORST',
        'USC',
        'STAN',
        'UTAH',
        'WASH',
        'WSU',
        ## SEC ##
        'ALA',
        'ARK',
        'AUB',
        'FLA',
        'UGA',
        'UK',
        'LSU',
        'MISS',
        'MIZ',
        'SC',
        'TA&M',
        'VAN',
        ## AMERICAN ##
        'TEM',
        'USF',
        'TULN',
        'NAVY',
        'MEM',
        'SMU',
        'UCF',
        'CIN',
        'TLSA',
        'ECU',
        'HOU',
        ## CONFERENCE USA ##
        'WKU',
        'MRSH',
        'ODU',
        'MTSU',
        'FAU',
        'CLT',
        'FIU',
        'UTSA',
        'UAB',
        'UNT',
        'UTEP',
        'RICE',
        'USM',
        'LT',
        ## INDEPENDENT ##
        'BYU', 
        'ARMY',
        'LIB',
        'NMSU',
        'MASS',
        'CONN',
        ## MID-AMERICAN ##
        'KENT',
        'M-OH',
        'OHIO',
        'BGSU',
        'BUFF',
        'AKR',
        'NIU',
        'CMU',
        'TOL',
        'BALL',
        'EMU',
        'WMU',
        ## MOUNTAIN WEST ##
        'USU',
        'AFA',
        'BSU',
        'WYO',
        'CSU',
        'UNM',
        'SDSU',
        'FRES',
        'NEV',
        'SJSU',
        'HAW',
        'UNLV',
        ## SUN BELT ##
        'APP',
        'GAST',
        'CCU',
        'TROY',
        'GASO',
        'UL',
        'TXST',
        'ULM',
        'USA',
        'ARST',
        #### FCS SCHOOLS ####
        ## ASUN ##
        'JVST',
        'CARK',
        'EKU',
        'KENN',
        'UNA',
        'APSU',
        ## BIG SKY ##
        'CP',
        'EWU',
        'IDHO',
        'MONT',
        'MTST',
        'NAU',
        'UNCO',
        'PRST',
        'SAC',
        'UCD',
        'WEB',
        'IDST',
        ## BIG SOUTH ##
        'BRY',
        'CAM',
        'CHSO',
        'GWEB',
        'NCAT',
        'RMU',
        ## CAA ##
        'ALB',
        'DEL',
        'ELON',
        'HAMP',
        'ME',
        'MONM',
        'UNH',
        'URI',
        'RICH',
        'STBK',
        'TOW',
        'VILL',
        'W&M',
        ## IVY ##
        'BRWN',
        'COLU',
        'COR',
        'DART',
        'HARV',
        'PENN',
        'PRIN',
        'YALE',
        ## MEAC ##
        'DSU',
        'MORG',
        'NORF',
        'NCCU',
        'SCST',
        'HOW',
        ## MISSOURI VALLEY ##
        'ILST',
        'INST',
        'MOST',
        'UND',
        'NDSU',
        'UNI',
        'SDAK',
        'SDST',
        'SIU',
        'WIU',
        'YSU',
        ## NORTHEAST ##
        'CCSU',
        'LIU',
        'MRMK',
        'SHU',
        'SFPA',
        'STO',
        'WAG',
        'DUQ',
        ## OHIO VALLEY ##
        'EIU',
        'LIN',
        'MUR',
        'SEMO',
        'TNST',
        'TNTC',
        'UTM',
        ## PATRIOT ##
        'BUCK',
        'COLG',
        'FOR',
        'GTWN',
        'HC',
        'LAF',
        'LEH',
        ## PIONEER ##
        "BUT",
        "DAV",
        "DAY",
        "DRKE",
        "MRST",
        "PRES",
        "USD",
        "STTHOM",
        "STET",
        "VAL",
        "MORE",
        ## SOUTHERN ##
        "MER",
        "UTC",
        "ETSU",
        "FUR",
        "SAM",
        "CIT",
        "VMI",
        "WCU",
        "WOF",
        ## SOUTHLAND ##
        "HBU",
        "UIW",
        "LAM",
        "MCN",
        "NICH",
        "NWST",
        "SELA",
        "TAMC",
        ## SWAC ##
        "ALST",
        "AAMU",
        "BCU",
        "JKST",
        "MVSU",
        "FAMU",
        "ALCN",
        "UAPB",
        "GRAM",
        "PV",
        "SOU",
        "TXSO",
        ## WAC ##
        "SHSU",
        "ACU",
        "SUU",
        "TAR",
        "UTU",
        "SFA",
        
    ]
    
    _LOGGER.debug("Team list: %s", team_list)
    return team_list


@config_entries.HANDLERS.register(DOMAIN)
class CollegeFootballScoresFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for College Football."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._data = {}
        self._errors = {}

    # async def async_step_import(self, user_input: dict[str, Any]) -> FlowResult:
    #     """Import a config entry."""

    #     user_input = user_input[DOMAIN]
    #     result: FlowResult = await self.async_step_user(user_input=user_input)
    #     if errors := result.get("errors"):
    #         return self.async_abort(reason=next(iter(errors.values())))
    #     return result

    async def async_step_user(self, user_input={}):
        """Handle a flow initialized by the user."""
        self._errors = {}
        self._team_list = _get_team_list()

        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title=self._data[CONF_NAME], data=self._data)
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""

        # Defaults
        defaults = {
            CONF_NAME: DEFAULT_NAME,
            CONF_TIMEOUT: DEFAULT_TIMEOUT,
            CONF_TEAM_ID: self._team_list,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=_get_schema(self.hass, user_input, defaults),
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CollegeFootballScoresOptionsFlow(config_entry)


class CollegeFootballScoresOptionsFlow(config_entries.OptionsFlow):
    """Options flow for College Football."""

    def __init__(self, config_entry):
        """Initialize."""
        self.config = config_entry
        self._errors = {}

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return await self._show_options_form(user_input)

    async def _show_options_form(self, user_input):
        """Show the configuration form to edit location data."""

        return self.async_show_form(
            step_id="init",
            data_schema=_get_schema(self.hass, user_input, self.config.data),
            errors=self._errors,
        )
