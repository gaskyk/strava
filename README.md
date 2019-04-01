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
2. Go to your profile, click [My Account](https://www.strava.com/account), click [Download or Delete Your Data](https://www.strava.com/athlete/delete_your_account) then `Get Started` button. Don't worry nothing gets deleted
3. Under point 2 click button `Request Your Archive`
4. Wait for an email to be sent (usually within a few hours)
5. Click the link in email to download zipped folder containing activities
6. You may see in the folder miscellaneous file extensions `.tcx`, `.tcx.gz` or `.gpx.gz` files. Unzip the .gz files so that only `.tcx` or `.gpx` files remain

### Run Python then R files

1. Take care to edit the file paths in each file
2. Ensure the `activities.csv` files is in the `INDIR` file directory

Data wrangling is done first using Python 3.6 in the file *Parse_GPX_and_TCX_to_CSV_add_attributes.py*. Packages required:
- gpxpy
- re
- os
- pandas
- numpy

Analysis and graphs are done after running the above code using R 3.4.3 in the file *strava_analysis.R*. Libraries required:
- chron
- tidyverse