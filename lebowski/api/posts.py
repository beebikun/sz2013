from lebowski import settings
from lebowski.settings import get_data

import urllib2
import json
import re

engineurl = "http://%(host)s:%(port)s/"%{'host':settings.LEBOWSKI['HOST'],'port':settings.LEBOWSKI['PORT']}

def main_post(data,prefix):
	req = urllib2.Request(engineurl+prefix)
	req.add_header('Content-Type', 'application/json')
	try:
		return json.loads(urllib2.urlopen(req, json.dumps(data)).read())
	except (urllib2.HTTPError,urllib2.URLError), e:
		reason,code = 'urllib2.HTTPError' in str(type(e)) and (e.reason,e.code) or (e,400)
		return {"data": str(reason), "status": code}


def main_get(data,prefix):  
    req = urllib2.Request(engineurl+prefix)
    req.add_header('Content-Type', 'application/json')
    return urllib2.urlopen(req).read()

def users_create(data):
	response = main_post(data,settings.LEBOWSKI['URLS']['USERS']['CREATE'])
	return get_data(response)
	

def places_create(data):
	response = main_post(data,settings.LEBOWSKI['URLS']['PLACES']['CREATE'])
	return get_data(response)

def messages_create(data):
	response = main_post(data,settings.LEBOWSKI['URLS']['MESSAGES']['CREATE'])
	return get_data(response)
