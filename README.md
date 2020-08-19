# pyNDFD-fetcher

This repository contains a repo with APIs for the National Digital Forecast Database Service. More info on the NDFD [HERE](https://www.weather.gov/mdl/ndfd_home)



## API calls

API Reference [HERE](https://graphical.weather.gov/xml/rest.php#use_it)

NDFD_Api.py contains many API calls for different NDFD data stores.

For example

 - Single Point Unsummarized Data: Returns DWML-encoded NDFD data for a point
 - Multiple Point Unsummarized Data: Returns DWML-encoded NDFD data for a list of points
 - A List of NDFD Points for a Subgrid
 - Data for subgrid defined by center point
 - NDFD data for a line
 - NDFD data for a specific zip code


More information on specific NDFD services can be found at https://graphical.weather.gov/xml/rest.php#use_it




Most API calls require a location in the form of a latitude and longitude, a start and end time, and which weather parameters you want predictions for. 

The returned data format is in an xml. The NDFD_Api.py contains several xml parsers, but the `_generalParseXml` is a general parser for the xml format. 



## Weather parameters

The API can return data for specific weather parameters. Below is a list of them.

List of possible elements


https://graphical.weather.gov/xml/docs/elementInputNames.php

 - Maximum Temperature:	maxt
 - Minimum Temperature:	mint
 - 3 Hourly Temperature: temp
 - Dewpoint Temperature: dew
 - Apparent Temperature: appt
 - 12 Hour Probability of Precipitation: pop12
 - Liquid Precipitation Amount: qpf
 - Snowfall Amount: snow
 - Cloud Cover Amount: sky
 - Relative Humidity: rh
 - Wind Speed: wspd
 - Wind Direction: wdir
 - Weather: wx
 - Weather Icons: icons
 - Wave Height: waveh
 - Probabilistic Tropical Cyclone Wind Speed >34 Knots (Incremental): incw34
 - Probabilistic Tropical Cyclone Wind Speed >50 Knots (Incremental): incw50
 - Probabilistic Tropical Cyclone Wind Speed >64 Knots (Incremental): incw64
 - Probabilistic Tropical Cyclone Wind Speed >34 Knots (Cumulative): cumw34
 - Probabilistic Tropical Cyclone Wind Speed >50 Knots (Cumulative): cumw50
 - Probabilistic Tropical Cyclone Wind Speed >64 Knots (Cumulative): cumw64
 - Wind Gust: wgust
 - Fire Weather from Wind and Relative Humidity: critfireo
 - Fire Weather from Dry Thunderstorms: dryfireo
 - Convective Hazard Outlook: conhazo
 - Probability of Tornadoes: ptornado
 - Probability of Hail: phail
 - Probability of Damaging Thunderstorm Winds: ptstmwinds
 - Probability of Extreme Tornadoes: pxtornado
 - Probability of Extreme Hail: pxhail
 - Probability of Extreme Thunderstorm Winds: pxtstmwinds
 - Probability of Severe Thunderstorms: ptotsvrtstm
 - Probability of Extreme Severe Thunderstorms: pxtotsvrtstm
 - Probability of 8- To 14-Day Average Temperature Above Normal: tmpabv14d
 - Probability of 8- To 14-Day Average Temperature Below Normal: tmpblw14d
 - Probability of One-Month Average Temperature Above Normal: tmpabv30d
 - Probability of One-Month Average Temperature Below Normal: tmpblw30d
 - Probability of Three-Month Average Temperature Above Normal: tmpabv90d
 - Probability of Three-Month Average Temperature Below Normal: tmpblw90d
 - Probability of 8- To 14-Day Total Precipitation Above Median: prcpabv14d
 - Probability of 8- To 14-Day Total Precipitation Below Median: prcpblw14d
 - Probability of One-Month Total Precipitation Above Median: prcpabv30d
 - Probability of One-Month Total Precipitation Below Median: prcpblw30d
 - Probability of Three-Month Total Precipitation Above Median: prcpabv90d
 - Probability of Three-Month Total Precipitation Below Median: prcpblw90d
 - Real-time Mesoscale Analysis Precipitation: precipa_r
 - Real-time Mesoscale Analysis GOES Effective Cloud Amount: sky_r
 - Real-time Mesoscale Analysis Dewpoint Temperature: td_r
 - Real-time Mesoscale Analysis Temperature: temp_r
 - Real-time Mesoscale Analysis Wind Direction: wdir_r
 - Real-time Mesoscale Analysis Wind Speed: wspd_r
 - Watches, Warnings, and Advisories: wwa
 - Ice Accumulation: iceaccum
 - Maximum Relative Humidity: maxrh
 - Minimum Relative Humidity: minrh

