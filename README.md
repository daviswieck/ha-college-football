[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
# College Football game data in Home Assistant

This integration fetches data for an College Football team's current/future game, and creates a sensor with attributes for the details of the game. 

The integration is a shameless fork of the excellent [ha-nfl](https://github.com/zacs/ha-nfl) custom component by @zacs. Thank you for doing all of the legwork! 
This also includes some work from [hass-nhlapi](https://github.com/JayBlackedOut/hass-nhlapi) custom component by @JayBlackedOut. Thank you for the lovelace help!
____________________________________________________________________________________________________________________________________________________________________

# MUST READ:
The default API in the "const.py" has a limit on amount of games it can pull. It defaults to all FBS schools, but only pulls the first 25 on the schedule. To get around this, you can update the "group" number in the API url for it to find your team. If you only care about the Top 25 teams, you can erase the "?groups=XX".

After install and restarting, navigate to
/config/custom_components/college_football/const.py
API_ENDPOINT = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80"
change "groups=XX" to one of the numbers below, ideally whichever conference your team is in. Restart HA and you should beable to find your team every week. 

## Conference Group Numbers
| Conference | Group Number |
| --- | --- |
| ALL FBS | 80 |
| ACC | 1 |
| AMERICAN | 151 |
| BIG12 | 4 |
| BIG10 | 5 |
| C-USA | 12 |
| FBS IND. | 18 |
| MAC | 15 |
| MOUNTAIN WEST | 17 |
| PAC12 | 9 |
| SEC | 8 |
| SUNBELT | 37 |
| FCS | 81 |
| ASUN | 176 |
| BIG SKY | 20 |
| BIG SOUTH | 40 |
| CAA | 18 |
| IVY | 22 |
| MEAC | 24 |
| MVFC | 21 |
| NEC | 25 |
| OVC | 26 |
| PATRIOT | 27 |
| PIONEER | 28 |
| SWAC | 31 |
| SOUTHERN | 29 |
| SOUTHLAND | 30 |
| WAC | 16 |
| DIVII/III | 35 |

## Sensor Data

### State
The sensor is pretty simple: the main state is `PRE`, `IN`, `POST`, or `NOT_FOUND`, but there are attributes for pretty much all aspects of the game, when available. State definitions are as you'd expect:
- `PRE`: The game is in pre-game state. This happens on the first day of the game week, which seems to be Tuesday evenings around midnight Eastern time (once all the games through the Monday Night Football game are wrapped up). 
- `IN`: The game is in progress.
- `POST`: The game has completed. 
- `BYE`: Your given team has a bye week this week. Note that attributes available are limited in this case (only abreviation, name, logo, and last updated time will be available). ONLY WORKS WITH NFL INTEGRATION, COLLEGE FOOTBALL API DOES NOT SHOW TEAMS ON BYE. 
- `NOT_FOUND`: There is no game found for your team, nor is there a bye. This should only happen at the end of the season, and once your team is eliminated from postseason play. WILL SHOW IF TEAM IS ON BYE. COLLEGE FOOTBALL API DOES NOT HAVE THE teamsonBye query in API. 

### Attributes
The attributes available will change based on the sensor's state, a small number are always available (team abbreviation, team name, and logo), but otherwise the attributes only populate when in the current state. The table below lists which attributes are available in which states. 

| Name | Value | Relevant States |
| --- | --- | --- |
| `date` | Date and time of the game | `PRE` `IN` `POST` |
| `kickoff_in` | Human-readable string for how far away the game is (eg. "in 30 minutes" or "tomorrow") |  `PRE` `IN` `POST` |
| `quarter` | The current quarter of gameplay | `IN` |
| `clock` | The clock value within the quarter (should never be higher than 15:00) | `IN` |
| `venue` | The name of the stadium where the game is being played (eg. "Arrowhead Stadium") | `PRE` `IN` `POST` |
| `location` | The city and state where the game is being played (eg. "Pittsburgh, PA") | `PRE` `IN` `POST` |
| `tv_network` | The TV network where you can watch the game (eg. "NBC" or "NFL"). Note that if there is a national feed, it will be listed here, otherwise the local affiliate will be listed. | `PRE` `IN` `POST` |
| `odds` | The betting odds for the game (eg. "PITT -5.0") | `PRE` |
| `overunder` | The over/under betting line for the total points scored in the game (eg. "42.5"). | `PRE` |
| `possession` | The ID of the team in possession of the ball. This will correlate to `team_id` or `opponent_id` below. Note that this value will be null in between posessions (after a score, etc). | `IN` |
| `last_play` | Sentence describing the most recent play, usually including the participants from both offense and defense, and the resulting yards. Note this can be null on posession changes or in between quarters. | `IN` |
| `down_distance_text` | String for the down and yards to go (eg. "2nd and 7"). | `IN` |
| `team_abbr` | The abbreviation for your team (ie. `TTU` for Texas Tech). | `PRE` `IN` `POST` `BYE` |
| `team_id` | A numeric ID for your team, used to match `possession` above. | `PRE` `IN` `POST` |
| `team_name` | Your team's name (eg. "Red Raiders"). Note this does not include the college name. | `PRE` `IN` `POST` `BYE` |
| `team_record` | Your team's current record (eg. "2-3"). | `PRE` `IN` `POST` |
| `team_homeaway` | Your team's home/away status. Either `home` or `away`. | `PRE` `IN` `POST` |
| `team_logo` | A URL for a 500px wide PNG logo for the team. | `PRE` `IN` `POST` `BYE` |
| `team_colors` | An array with two hex colors. The first is your team's primary color, and the second is their secondary color.  | `PRE` `IN` `POST` |
| `team_score` | Your team's score. An integer. | `IN` `POST` |
| `team_rank` | Your team's rank. An integer. Note: If rank is 99, then team is UNRANKED | `IN` `POST` |
| `team_win_probability` | The real-time chance your team has to win, according to ESPN. A percentage, but presented as a float. Note that this value can become null in between posession changes. | `IN` |
| `team_timeouts` | The number of remaining timeouts your team has. | `PRE` `IN` `POST` |
| `opponent_abbr` | The abbreviation for your opponent (ie. `UT` for the Longhorns). | `PRE` `IN` `POST` `BYE` |
| `opponent_id` | A numeric ID for your opponent, used to match `possession` above. | `PRE` `IN` `POST` |
| `opponent_name` | Your opponent's name (eg. "Longhorns"). Note this does not include the college name. | `PRE` `IN` `POST` `BYE` |
| `opponent_record` | Your opponent's current record (eg. "2-3"). | `PRE` `IN` `POST` |
| `opponent_homeaway` | Your opponent's home/away status. Either `home` or `away`. | `PRE` `IN` `POST` |
| `opponent_logo` | A URL for a 500px wide PNG logo for the opponent. | `PRE` `IN` `POST` `BYE` |
| `opponent_colors` | An array with two hex colors. The first is your opponent's primary color, and the second is their secondary color. | `PRE` `IN` `POST` |
| `opponent_score` | Your opponent's score. An integer. | `IN` `POST` |
| `opponent_rank` | Your opponent's rank. An integer. Note: If rank is 99, then team is UNRANKED | `IN` `POST` |
| `opponent_win_probability` | The real-time chance your opponent has to win, according to ESPN. A percentage, but presented as a float. Note that this value can become null in between posession changes. | `IN` |
| `opponent_timeouts` | The number of remaining timeouts your opponent has. | `PRE` `IN` `POST` |
| `last_update` | A timestamp for the last time data was fetched for the game. If you watch this in real-time, you should notice it updating every 10 minutes, except for during the game (and for the ~20 minutes pre-game) when it updates every 5 seconds. | `PRE` `IN` `POST` `BYE` |

## Installation

### Manually

Clone or download this repository and copy the "college-football" directory to your "custom_components" directory in your config directory

```<config directory>/custom_components/college-football/...```
  
### HACS

1. Open the HACS section of Home Assistant.
2. Click the "..." button in the top right corner and select "Custom Repositories."
3. In the window that opens paste this Github URL.
4. In the window that opens when you select it click om "Install This Repository in HACS"
  
## Configuration

You'll need to know your team ID, which is a 2- to 4-letter acronym (eg. "TTU" for Texas Tech or "UT" for Texas). This MUST BE capital letters. You can find yours at https://https://www.espn.com/college-football/ in the top scores UI. 

### Via the "Configuration->Integrations" section of the Home Assistant UI

Look for the integration labeled "college_football" and enter your team's acronym in the UI prompt. You can also enter a friendly name. If you keep the default, your sensor will be `sensor.college_football`, otherwise it will be `sensor.friendly_name_you_picked`. 

### Manually in your `configuration.yaml` file

To create a sensor instance add the following configuration to your sensor definitions using the team_id found above:

```
- platform: college_football
  team_id: 'TTU'
```

After you restart Home Assistant then you should have a new sensor called `sensor.college_football` in your system.

You can overide the sensor default name (`sensor.college_football`) to one of your choosing by setting the `name` option:

```
- platform: college_football
  team_id: 'TTU'
  name: Texas Tech Red Raiders
```

Using the configuration example above the sensor will then be called "sensor.texas_tech_red_raiders".

