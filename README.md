# Strava

## Overview

Import .gpx files of activities recorded on [Strava](https://www.strava.com/) and analyse those activities to:
- Create maps of runs or cycle rides
- Show elevations encountered
- The speed of runs or cycle rides (in km/h)
- How the speed varies based on the length of the activity

## How do I use this project?

Data wrangling is done using Python 3.6 in the file *Parse_GPX_to_CSV_add_attributes.py*. Packages required:
- gpxpy
- os
- pandas
- numpy

Analysis and graphs are done using R 3.4.3 in the file *strava_analysis.R* with inspiration and code from [Marcus Volz](https://github.com/marcusvolz/strava). Libraries required:
- chron
- tidyverse
