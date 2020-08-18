#python3
"""API for fetching NDFD data via their rest service. Written in python 3. In development.
Right now subGrid and getDataZipcode work well.
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
import json
from datetime import timedelta, datetime



class ApiError(Exception):

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        print(self.message)
        raise Exception(self.message + ' ' + str(self.status_code))

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        print(rv['message'])
        return rv

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
	return urlString

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

	return urlString

"""
Unsummarized Data for a Subgrid:
 Returns DWML-encoded NDFD data for a subgrid defined by a lower left and upper right point
"""
###THIS API DOES NOT WORK
def subGridCornerPoints(lat1, lon1, lat2, lon2, resolutionSub, product, begin, end, Unit='m', optional_params=['wspd', 'wdir']):
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

	return urlString

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

Parameters:
zipcodes: String of zipcodes seperated by a space ie '22152 22150 xxxxx '
product: string of type of product, for this make sure it is 'time-series'
begin: string of beginning time in 'YYYY-MM-DDT00:00:00'
end: string of end time in 'YYYY-MM-DDT00:00:00'
optional_params: list of strings of weather properties to watch

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

Parameters:
centerPointLat/centerPointLon: string of coords of center point of grid
distanceLat/distanceLon: string of latitudinal distances and longitudinal distances
resolutionSquare: string of resolution of grid. Smallest is ~ 5km
product: string of type of product, for this make sure it is 'time-series'
begin: string of beginning time in 'YYYY-MM-DDT00:00:00'
end: string of end time in 'YYYY-MM-DDT00:00:00'
unit: string of imperial or metric units
optional_params: list of strings of weather properties to watch



"""

def subGrid(centerPointLat, centerPointLon, distanceLat, distanceLon, resolutionSquare, product, begin, end, Unit, optional_params):
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

def line(endPoint1Lat, endPoint1Lon, endPoint2Lat, endPoint2Lon, product, begin, end, Unit='m', optional_params=['wspd', 'wdir']):
	#Split into 3 dictionaries, each are encoded in a different manner
	params = {
		'endPoint1Lat':endPoint1Lat,
		'endPoint1Lon':endPoint1Lon,
		'endPoint2Lat':endPoint2Lat,
		'endPoint2Lon':endPoint2Lon,
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
#Not complete
# def subGridDayWise(centerPointLat, centerPointLon, distanceLat, distanceLon, resolutionSquare, startDate, numDays):
# 	params = {
# 		'centerPointLat': centerPointLat,
# 		'centerPointLon': centerPointLon,
# 		'distanceLat': distanceLat,
# 		'distanceLon': distanceLon,
# 		'resolutionSquare': resolutionSquare,
# 		'startDate': startDate,
# 		'numDays':numDays
# 	}
# 	return urlencode(params, doseq=True)

#Main URL path
def _url(path=''):
    return 'http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?' + path


#This function acts as a general xml parser
def _generalParseXml(data):
	o = xmltodict.parse(data.content)
	d = json.dumps(o)
	d = json.loads(d)
	return d


#Still in dev, now returns values for certain methods
def _customParseXml(data):
	outDict = {}
	#Load xml object into dictionary
	d = xmltodict.parse(data.content)	
	#use dataDict as base content dictionary, we only care about this
	dataDict = d['dwml']['data']
	print(dataDict)
	#Put list of points  into outDict, lat and long are now called @latitude and @longitude
	for key in dataDict['location']:
		outDict[key['location-key']] = [{'loc':key['point']}]
	#Make a faux list called locationsList. This is iterated over to fill outDict for now because xml structure is annoying.
	locationsList = list(outDict.keys())
	for i in range(len(locationsList)):
		for j in range(len((dataDict['parameters'][i]['wind-speed']['value']))):
			outDict[locationsList[i]].append({'wind-speed':dataDict['parameters'][i]['wind-speed']['value'][j]})
			outDict[locationsList[i]].append({'wind-direction':dataDict['parameters'][i]['direction']['value'][j]})
			outDict[locationsList[i]].append({'time':dataDict['time-layout']['start-valid-time'][j]})
	#Maybe make time stamp a key for other info
	#For structure is:
	"""
	outDict = {
		'point1':{[
			{'loc':{(@latitude, '00.00'), (@longitude, '00.00')}},
			{'wind-speed':'6'}, 
			{'wind-direction':'9'}, 
			{'time':2020-02-06T22:00:00-05:00'}]
		}
		'point2':{same struct as above},
		'pointxx'
	}
	"""
	return outDict


#Still in dev, may combine with general _customParseXml function
def _customParseXmlSinglePoint(data):
	#outDict is output structure, convieniently parsed
	outDict = {}
	d = xmltodict.parse(data.content)	
	#use dataDict as base content dictionary, we only care about this
	#locKey is key to the point in question. in the single point querery, it is point1
	#Lats and lons
	locs = d['dwml']['data']['location']
	locKey = locs['location-key']
	lat = locs['point']['@latitude']
	lon = locs['point']['@longitude']
	outDict[locKey] = {'latitude':lat, 'longitude':lon}
	outDict[locKey]['data'] = []
	#now begins the parsing of the xml body. It is not the most efficient logic as of now
	#but im sure this can be fixed!
	for i in (d['dwml']['data']['time-layout']['start-valid-time']):
		outDict[locKey]['data'].append([{'datetime':i}])
	params = list((d['dwml']['data']['parameters'].keys()))
	for param in range(1,len(params)):
		idx = 0
		for value in d['dwml']['data']['parameters'][params[param]]['value']:
			outDict[locKey]['data'][idx].append({params[param]:value})
			idx+=1

	return outDict




def run_request(q):
	print(_url(q))
	resp = requests.get(_url(q))
	if resp.status_code != 200:
		# This means something went wrong.
		raise ApiError(resp.text, resp.status_code)
	return resp

#test each API call
def run_tests(_tests):
	for key, val in _tests.items():
		try:
			run_request(val)
			print('*************** QUERY ', key, " HAS SUCCEEDED ************")
		except:
			print('*************** QUERY ', key, " FAILED ************")
			print("en error ocurred")
			e = sys.exc_info()[0]
			print(e)


_tests={
	'q1':singlePointDataQuery('37.33', '-122.03','time-series', str(datetime.now().isoformat()), str((datetime.now()+timedelta(days=1)).isoformat())),
	'q2':listPointDataQuery('time-series', str(datetime.now().isoformat()), str((datetime.now()+timedelta(days=1)).isoformat())),
	# 'q3':subGridCornerPoints('35.00', '-82.00', '35.5', '-81.50', '20.0', 'time-series', '2020-02-09T17:00:00', '2020-02-09T18:00:00'),
	'q4':listCoordsInGrid('35.00', '-82.00', '35.50', '-81.50', '20.0'),
	'q5':getDataZipcode('22152 22150', 'time-series', str(datetime.now().isoformat()), str((datetime.now()+timedelta(days=1)).isoformat())),
	# 'q6':subGrid('38.0', '-97.4', '4.0', '4.0', '0.001' ,'time-series','2020-02-01T17:00:00','2020-02-01T18:00:00'),
	'q7':subGrid('40.7128', '-74.0060', '1.0', '1.0', '1.0' ,'time-series',str(datetime.now().isoformat()), str((datetime.now()+timedelta(days=1)).isoformat()),Unit='m', optional_params=['wspd', 'wdir']),
	# 'q8':subGridDayWise('38.0', '-97.4', '5.0', '5.0', '5.0', '2020-02-04', '1')
	#Test from Dominion Roseland Substation
	'q9':line('38.723', '-77.288854', '38.7499', '-77.339','time-series',str(datetime.now().isoformat()), str((datetime.now()+timedelta(days=1)).isoformat()))
	}

################################ Here Begins induvidual data requests #############################################
def getSubGridData(centerLat, centerLon, distanceLat, distanceLon, resolutionSquare, product='time-series', begin=str(datetime.now().isoformat()), end=str((datetime.now()+timedelta(days=+1)).isoformat()), Unit='m', optional_params=['critfireo']):
	data = run_request(subGrid(centerLat, centerLon, distanceLat, distanceLon, resolutionSquare, product, begin, end, Unit, optional_params))
	outData = _generalParseXml(data)
	return outData


if __name__ == '__main__':
	run_tests(_tests)



	# lat = 40.758701
	# lon = -111.876183
	# dist = 20
	# resolution = 10
	# start = str(datetime.now().isoformat())
	# end = str((datetime.now()+timedelta(days=1)).isoformat())
	# print(start, end)
	# # start = '2020-08-20T00:00:00'
	# # end = '2020-08-21T00:00:00'

	# data = getSubGridData(str(lat), str(lon), str(dist), str(dist), str(resolution), 'time-series', start, end)
	# print(data)

