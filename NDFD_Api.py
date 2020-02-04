#python3
"""API for fetching NDFD data via their rest service. Written in python 3. In development
API Reference: https://graphical.weather.gov/xml/rest.php#degrib
Author: Tuomas Talvitie
Year: 2020
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
from urllib.parse import urlencode, quote
import xml.etree.ElementTree as ET
import xmltodict


# start = datetime.datetime.today() + datetime.timedelta(days=1)
# end = datetime.datetime.today() + datetime.timedelta(days=2)

# params = {'lat1':'33.8835', 'lon1':'-80.0679', 'lat2':'33.8835', 'lon2':'-80.0679', 'resolutionSub':'5', 'product':'time-series', 'begin':'2020-02-01T17:12:35', 'end':'2020-06-02T17:12:35', 'appt':'appt', 'rh':'rh', "temp_r":"temp_r", "temp":"temp" }

# print(urlencode({'zipCodeList':'20190 25414'}))
"""
Single Point Unsummarized Data: Returns DWML-encoded NDFD data for a point
"""
#Works
def singlePointDataQuery(lat1, lon1, product, begin, end, Unit='m', optional_params=['wspd', 'wdir']):
	params = {
		'lat':lat1,
		'lon':lon1,
		'product':product
	}
	params2 = {'begin':begin,
	'end':end
	}
	params3 = {
		'Unit':Unit,
	}
	urlString = urlencode(params)
	subString = ''
	for key, value in params2.items():
		subString += '&'+str(key) + '=' + str(value)
	urlString+=subString
	for i in optional_params:
		params3[i] = i
	urlString +='&' + urlencode(params3)

	return urlencode(params)

"""
Multiple Point Unsummarized Data: Returns DWML-encoded NDFD data for a list of points
"""

#Works, but need to parse the list of coords legibly first. But API does work.
def listPointDataQuery(product, begin, end, listLatLon=('38.99,-77.02 39.70,-104.80'), Unit='m', optional_params=['wspd', 'wdir']):
	params = {
		'listLatLon':listLatLon,
		'product':product
	}

	params2 = {'begin':begin,
	'end':end
	}
	params3 = {
		'Unit':Unit,
	}
	urlString = urlencode(params)
	subString = ''
	for key, value in params2.items():
		subString += '&'+str(key) + '=' + str(value)
	urlString+=subString
	for i in optional_params:
		params3[i] = i
	urlString +='&' + urlencode(params3)

	return urlencode(params)

"""
Unsummarized Data for a Subgrid:
 Returns DWML-encoded NDFD data for a subgrid defined by a lower left and upper right point
"""
###Deprecated, examples online dont work
def subGridDataQuery(lat1, lon1, lat2, lon2, resolutionSub, product, begin, end, Unit='m', optional_params=['wspd', 'wdir']):
	params = {
		'lat1':lat1,
		'lon1':lon1,
		'lat2':lat2,
		'lon2':lon2,
		'resolutionSub':resolutionSub,
		'product':product
	}
	params2 = {'begin':begin,
	'end':end
	}
	params3 = {
		'Unit':Unit,
	}
	urlString = urlencode(params)
	subString = ''
	for key, value in params2.items():
		subString += '&'+str(key) + '=' + str(value)
	urlString+=subString
	for i in optional_params:
		params3[i] = i
	urlString +='&' + urlencode(params3)

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

def subGrid(centerPointLat, centerPointLon, distanceLat, distanceLon, resolutionSquare, product, begin, end, Unit='m', optional_params=['wspd', 'wdir']):
	#Split into 3 dictionaries, each are encoded in a different manner
	params = {
		'centerPointLat':centerPointLat,
		'centerPointLon':centerPointLon,
		'distanceLat':distanceLat,
		'distanceLon':distanceLon,
		'resolutionSquare':resolutionSquare,
		'product':product
	}
	#Begin/end has special encoding
	params2 = {'begin':begin,
	'end':end
	}
	params3 = {
		'Unit':Unit,
	}

	urlString = urlencode(params)
	subString = ''
	for key, value in params2.items():
		subString += '&'+str(key) + '=' + str(value)
	urlString+=subString
	for i in optional_params:
		params3[i] = i
	urlString +='&' + urlencode(params3)

	return urlString

#For daywise
def subGridDayWise(centerPointLat, centerPointLon, distanceLat, distanceLon, resolutionSquare, startDate, numDays):
	params = {
		'centerPointLat': centerPointLat,
		'centerPointLon': centerPointLon,
		'distanceLat': distanceLat,
		'distanceLon': distanceLon,
		'resolutionSquare': resolutionSquare,
		'startDate': startDate,
		'numDays':numDays
	}
	return urlencode(params, doseq=True)

#Main URL path
def _url(path=''):
    return 'http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?' + path




#Still in dev, now returns values
def parseXml(data):
	root = ET.fromstring(data.content)
	print(root)
	# for child in root.iter('*'):
 #   		print(child.tag, child.attrib)
	# for child in root.iter('*'):
	# 	print(child.tag, child.text)
	# for i in root.xpath("//time-layout"):
	# 	print(i)
	d = xmltodict.parse(data.content)	
	dataDict = d['dwml']['data']
	for key, val in dataDict.items():
		print(key, val)
	return 



def run_request(q):
	print(_url(q))
	resp = requests.get(_url(q))
	if resp.status_code != 200:
		# This means something went wrong.
		print(resp.status_code)
		raise ApiError('GET /tasks/ {}'.format(resp.status_code))
	return resp

#test each API call
def run_tests(_tests):
	for i in _tests.keys():
		try:
			run_request(_tests[i])
			print('*************** QUERY ', i, " HAS SUCCEEDED ************")
		except:
			print('*************** QUERY ', i, " FAILED ************")
			print("en error ocurred")
			e = sys.exc_info()[0]
			print(e)


_tests={
	'q1':singlePointDataQuery('37.33', '-122.03','time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35'),
	'q2':listPointDataQuery('time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35'),
	'q3':subGridDataQuery('35.00', '-82.00', '35.5', '-81.50', '20.0', 'time-series', '2020-02-09T17:00:00', '2020-02-09T18:00:00'),
	'q4':listCoordsInGrid('35.00', '-82.00', '35.50', '-81.50', '20.0'),
	'q5':getDataZipcode('20190 25414', 'time-series', '2020-02-01T17:12:35', '2020-06-02T17:12:35' ),
	# 'q6':subGrid('38.0', '-97.4', '4.0', '4.0', '0.001' ,'time-series','2020-02-01T17:00:00','2020-02-01T18:00:00'),
	'q7':subGrid('40.7128', '-74.0060', '1.0', '1.0', '1.0' ,'time-series','2020-02-04T20:00:00','2020-02-04T20:00:00'),
	# 'q8':subGridDayWise('38.0', '-97.4', '5.0', '5.0', '5.0', '2020-02-04', '1')
	}



if __name__ == '__main__':
	# data=run_request(_tests['q7'])
	# print(data.content)
	# run_tests(_tests)
	# parseXml(data)



