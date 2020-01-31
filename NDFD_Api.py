#python3
"""API for fetching NDFD data via their rest service. Written in python 3. In development
API Reference: https://graphical.weather.gov/xml/rest.php#degrib
Author: Tuomas Talvitie
Year: 2020
"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
from urllib.parse import urlencode, quote

# start = datetime.datetime.today() + datetime.timedelta(days=1)
# end = datetime.datetime.today() + datetime.timedelta(days=2)

# params = {'lat1':'33.8835', 'lon1':'-80.0679', 'lat2':'33.8835', 'lon2':'-80.0679', 'resolutionSub':'5', 'product':'time-series', 'begin':'2020-02-01T17:12:35', 'end':'2020-06-02T17:12:35', 'appt':'appt', 'rh':'rh', "temp_r":"temp_r", "temp":"temp" }

# print(urlencode({'zipCodeList':'20190 25414'}))
"""
Single Point Unsummarized Data: Returns DWML-encoded NDFD data for a point
"""
#Works
def singlePointDataQuery(lat1, lon1, product, begin, end, optional_params=['wspd', 'wdir']):
	params = {
		'lat':lat1,
		'lon':lon1,
		'product':product,
		'begin':begin,
		'end':end,
	}
	for i in optional_params:
		params[i] = i


	return urlencode(params)

"""
Multiple Point Unsummarized Data: Returns DWML-encoded NDFD data for a list of points
"""

#Works, but need to parse the list of coords legibly first. But API does work.
def listPointDataQuery(product, begin, end, listLatLon=('38.99,-77.02 39.70,-104.80'), optional_params=['wspd', 'wdir']):
	params = {
		'listLatLon':listLatLon,
		'product':product,
		'begin':begin,
		'end':end,
	}
	for i in optional_params:
		params[i] = i


	return urlencode(params)

"""
Unsummarized Data for a Subgrid:
 Returns DWML-encoded NDFD data for a subgrid defined by a lower left and upper right point
"""
###Deprecated, examples online dont work
def subGridDataQuery(lat1, lon1, lat2, lon2, resolutionSub, product, begin, end, optional_params=['wspd', 'wdir']):
	params = {
		'lat1':lat1,
		'lon1':lon1,
		'lat2':lat2,
		'lon2':lon2,
		'resolutionSub':resolutionSub,
		'product':product,
		'begin':begin,
		'end':end,
	}
	for i in optional_params:
		params[i] = i

	return urlencode(params)

"""A List of NDFD Points for a Subgrid: Returns the WGS84 latitude and longitude 
values of all the NDFD grid points within a rectangular subgrid as defined by points 
at the lower left and upper right corners of the rectangle. The returned list of points 
is suitable for use in inputs listLatLon and gmlListLatLon. 
NOTE: The subgrid locations will only form a rectangle when viewed in the NDFD 
projection applicable to the grid.
"""

#Works
def listCoordsInGrid(listLat1, listLon1, listLat2, listLon2, resolutionList):
	params = {
		'listLat1': listLat1,
		'listLon1': listLon1,
		'listLat2': listLat2,
		'listLon2': listLon2,
		'resolutionList': resolutionList
	}
	return urlencode(params)

"""
Unsummarized Data for One or More Zipcodes: 
Returns DWML-encoded NDFD data for one or more zip codes 
(50 United States and Puerto Rico). The returned list of points is suitable for use in 
inputs listLatLon and gmlListLatLon.
"""

#Works and works well
def getDataZipcode(zipcodes, product, begin, end, optional_params=['wspd', 'wdir']):
	params = {
		'zipCodeList': zipcodes,
		'product': product,
		'begin': begin,
		'end': end
	}
	for i in optional_params:
		params[i] = i
	return urlencode(params)

"""
Unsummarized Data for a Subgrid Defined by a Center Point: 
Returns DWML-encoded NDFD data for a rectangle defined by a center point and 
distances in the latitudinal and longitudinal directions.
"""

def subGrid(centerPointLat, centerPointLon, distanceLat, distanceLon, resolutionSquare, product, begin, end, optional_params=['wspd', 'wdir']):
	params = {
		'centerPointLat':centerPointLat,
		'centerPointLon':centerPointLon,
		'distanceLat':distanceLat,
		'distanceLon':distanceLon,
		'resolutionSquare':resolutionSquare,
		'product':product,
		'begin':begin,
		'end':end,
	}
	for i in optional_params:
		params[i] = i
	return urlencode(params)



# raise Exception
def _url(path=''):
    return 'http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?' + path

def _run(q):

	print(_url(q))
	resp = requests.get(_url(q))
	if resp.status_code != 200:
		# This means something went wrong.
		print(resp.status_code)
		raise ApiError('GET /tasks/ {}'.format(resp.status_code))
	print(resp.content)


def _run_tests(_tests):
	for i in _tests.keys():
		_run(_tests[i])
		print('*************** QUERY ', i, " HAS SUCCEEDED ************")

_tests={

	'q1':subGridDataQuery('35.00', '-82.00', '35.5', '-81.50', '20.0', 'time-series', '2020-02-01T17:00:00', '2020-02-02T18:00:00'),
	'q2':singlePointDataQuery('37.33', '-122.03','time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35'),
	'q3':listPointDataQuery('time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35'),
	'q4':listCoordsInGrid('35.00', '-82.00', '35.50', '-81.50', '20.0'),
	'q5':getDataZipcode('20190 25414', 'time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35' ),
	'q6':subGrid('38.0', '-97.4', '50.0', '50.0', '20.0' ,'time-series','2020-02-01T17:00:00','2020-02-02T18:00:00')
	}



if __name__ == '__main__':
	_run(_tests['q6'])
	# _run_tests(_tests)


