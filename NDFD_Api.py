#python3 test env

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
from urllib.parse import urlencode, quote

# from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP
start = datetime.datetime.today() + datetime.timedelta(days=1)
end = datetime.datetime.today() + datetime.timedelta(days=2)

#Test below
# http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=37.33&lon=-122.03&product=time-series&begin=2020-02-01T17:12:35&end=2020-06-02T17:12:35&appt=appt&rh=rh&temp_r=temp_r&temp=temp
# resp = requests.get('https://todolist.example.com/tasks/')
# if resp.status_code != 200:
#     # This means something went wrong.
#     raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))

params = {'lat1':'33.8835', 'lon1':'-80.0679', 'lat2':'33.8835', 'lon2':'-80.0679', 'resolutionSub':'5', 'product':'time-series', 'begin':'2020-02-01T17:12:35', 'end':'2020-06-02T17:12:35', 'appt':'appt', 'rh':'rh', "temp_r":"temp_r", "temp":"temp" }

print(urlencode({'listLatLon':('38.99,-77.02 39.70,-104.80')}))

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


###Deprecated 
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

q1 = (subGridDataQuery('35.00', '-82.00', '35.5', '-81.50', '20.0', 'time-series', '2020-02-01T17:00:00', '2020-02-0`T18:00:00'))

q2 = singlePointDataQuery('37.33', '-122.03','time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35')

q3 = listPointDataQuery('time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35')

# raise Exception
def _url(path=''):
    return 'http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?' + path
print(_url(q3))




resp = requests.get(_url(q3))
if resp.status_code != 200:
	# This means something went wrong.
	print(resp.status_code)
	raise ApiError('GET /tasks/ {}'.format(resp.status_code))
print(resp.content)


