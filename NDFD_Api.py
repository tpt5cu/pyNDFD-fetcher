#python3 test env

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
from urllib.parse import urlencode, quote

# from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP
start = datetime.datetime.today() + datetime.timedelta(days=1)
end = datetime.datetime.today() + datetime.timedelta(days=2)

params = {'lat1':'33.8835', 'lon1':'-80.0679', 'lat2':'33.8835', 'lon2':'-80.0679', 'resolutionSub':'5', 'product':'time-series', 'begin':'2020-02-01T17:12:35', 'end':'2020-06-02T17:12:35', 'appt':'appt', 'rh':'rh', "temp_r":"temp_r", "temp":"temp" }

# print(urlencode({'zipCodeList':'20190 25414'}))

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


def subGrid()

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

	'q1':subGridDataQuery('35.00', '-82.00', '35.5', '-81.50', '20.0', 'time-series', '2020-02-01T17:00:00', '2020-02-0`T18:00:00'),
	'q2':singlePointDataQuery('37.33', '-122.03','time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35'),
	'q3':listPointDataQuery('time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35'),
	'q4':listCoordsInGrid('35.00', '-82.00', '35.50', '-81.50', '20.0'),
	'q5':getDataZipcode('20190 25414', 'time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35' )
	}



if __name__ == '__main__':
	_run(_tests['q5'])
	# _run_tests(_tests)


