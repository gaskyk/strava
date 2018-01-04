# Strava

## Overview

Import .gpx files of activities recorded on [Strava](https://www.strava.com/) and analyse those activities to:
- Create maps of runs or cycle rides
- Show elevations encountered
- The speed of runs or cycle rides (in km/h)
- How the speed varies based on the length of the activity

The inspiration for this project and some R code comes from [Marcus Volz](https://github.com/marcusvolz/strava).

## How do I use this project?

### Bulk export from Strava

1. Log in to [Strava](https://www.strava.com/)
2. Select "[Settings](https://www.strava.com/settings/profile)" from the main drop-down menu at top right of the screen
3. Select "Download all your activities" from lower right of screen
4. Wait for an email to be sent
5. Click the link in email to download zipped folder containing activities
6. Unzip files

### Run Python then R files

Take care to edit the file paths in each file

Data wrangling is done first using Python 3.6 in the file *Parse_GPX_to_CSV_add_attributes.py*. Packages required:
- gpxpy
- os
- pandas
- numpy

Analysis and graphs are done after running the above code using R 3.4.3 in the file *strava_analysis.R*. Libraries required:
- chron
- tidyverse
