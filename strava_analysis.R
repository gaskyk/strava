###############################################
###                                         ###
###  Analyse my Strava activity             ###
###  2 January 2018                         ###
###  Inspiration and code thanks            ###
###  to Marcus Volz:                        ###
###  https://github.com/marcusvolz/strava   ###
###                                         ###
###############################################


## Import libraries
library(chron)
library(tidyverse)

## Import csv data from Python
tracks <- read.csv('C:/Users/ONS-BIG-DATA/Documents/Strava/activities_csv/activities.csv')

## Convert segment_time and cum_time to time format
format_time <- function(x) {
  x <- as.character(x)
  x <- gsub("0 days ", "",x, fixed=TRUE)
  x <- gsub(".000000000", "", x, fixed=TRUE)
  x <- strptime(x, "%T")
  x <- times(format(x, "%H:%M:%S"))
  
  return(x)
}

tracks$segment_time <- format_time(tracks$segment_time)
tracks$cum_time <- format_time(tracks$cum_time)

## Create a summary for each activity
tracks[is.na(tracks)] <- 0
tracks$Date <- as.Date(tracks$Timestamp)
track_summary <- tracks %>%
  dplyr::group_by(Track_number) %>%
  dplyr::summarise(cum_distance = max(cum_dist),
                   cum_time = max(cum_time),
                   type = first(Activity),
                   date = first(Date))
track_summary$speed_km <- as.numeric(track_summary$cum_distance/track_summary$cum_time/24)

## Plot average speed over time by type (ride or run)
ggplot(data=track_summary, aes(x=date, y=speed_km, group = type)) + geom_line() +
  labs(x="Date", y="Average speed (km/h)", title="Average speed over time") +
  ylim(0,25) + facet_grid(type ~ .) + theme(plot.title = element_text(hjust = 0.5))

## Plot length of ride / run by speed
ggplot(data=track_summary, aes(x=cum_distance, y=speed_km, group = type)) + geom_point() +
  labs(x="Length of activity (km)", y="Average speed (km/h)", title="Average speed by distance") +
  ylim(0,25) + facet_grid(. ~ type, scales="free") + theme(plot.title = element_text(hjust = 0.5))

## Produce a facet plot map of all rides / runs
ggplot() + geom_path(ggplot2::aes(Longitude, Latitude, group = Track_number, colour=Activity), tracks, size = 0.35, lineend = "round") +
  facet_wrap(~Track_number, scales = "free") +
  theme(panel.spacing = ggplot2::unit(0, "lines"),
        strip.background = ggplot2::element_blank(),
        strip.text = ggplot2::element_blank(),
        plot.margin = ggplot2::unit(rep(1, 4), "cm"),
        axis.line=element_blank(),axis.text.x=element_blank(),
        axis.text.y=element_blank(), axis.title.x=element_blank(),
        axis.title.y=element_blank(), panel.background=element_blank(),panel.border=element_blank(),panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),plot.background=element_blank(),
        axis.ticks = element_blank()) +
  scale_color_manual(values=c("blue", "green", "red"))

## Plot elevations
plot_elevations <- function(tracks) {
  # Compute total distance for each activity
  dist <- tracks %>%
    dplyr::group_by(Track_number) %>%
    dplyr::summarise(dist = max(cum_dist))
  
  # Normalise distance
  tracks <- tracks %>%
    dplyr::left_join(dist, by = "Track_number") %>%
    dplyr::mutate(dist_scaled = cum_dist / dist) %>%
    dplyr::arrange(Track_number, cum_dist)
  
  # Create plot
  p <- ggplot2::ggplot() +
    ggplot2::geom_line(ggplot2::aes(dist_scaled, Elevation, group = Track_number), tracks, alpha = 0.75) +
    ggplot2::facet_wrap(~Track_number) +
    ggplot2::theme_void() +
    ggplot2::theme(panel.spacing = ggplot2::unit(0, "lines"),
                   strip.background = ggplot2::element_blank(),
                   strip.text = ggplot2::element_blank(),
                   plot.margin = ggplot2::unit(rep(1, 4), "cm"))
  p
}

plot_elevations(tracks)


