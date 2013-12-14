# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import status
from sz.api import response as sz_api_response, serializers
from rest_framework.reverse import reverse
from sz.api.views import SzApiView
from sz.core import models, gis as gis_core
from sz.settings import LEBOWSKI_MODE_TEST
from sz import mode_test
import random
import shelve

def generate_places(list_len=100,places=[]):
    def generate_float():
        return round(random.uniform(0.000001, mode_test.STEP*mode_test.COUNT),6)
    if list_len:
        p = {
            'name':mode_test.PLACES_NAMES[random.randint(0,len(mode_test.PLACES_NAMES)-1)],
            u'location':{'lng':generate_float(),'lat':generate_float()}
        }    
        places.append(p)
        return generate_places(list_len-1,places)
    else:
        return places

def get_params(p):
    return dict(name=p['name'], city_id=0,
        position=gis_core.ll_to_point(p['location']['lng'],p['location']['lat']))
    
def place_serializers(p):
    return dict(city_id=0,place_name=p['name'],
    	place_latitude=p['location']['lat'], place_longitude=p['location']['lng'])

model_p = models.Place.objects
class GeneratePlaces(SzApiView):
    def get(self, request,format=None):    
        if not LEBOWSKI_MODE_TEST:
            return sz_api_response.Response({'data':'LEBOWSKI_MODE_TEST is off'})     
        old_places = shelve.open('generated_place.shelve')
        for p in old_places.get('venues',[]):
            model_p.filter(**get_params(p)).delete()
        data = {'venues':[]}
        place_count = request.QUERY_PARAMS.get('count', 100)
        places_list = generate_places(place_count)
        shelve.open('generated_place.shelve')['venues'] = places_list
        for p in places_list:
            place = place_serializers(p)
            data['venues'].append(place)
        return sz_api_response.Response(data) 

class GetPlaces(SzApiView):
    def get(self, request,format=None):    
        places_list = shelve.open('generated_place.shelve')['venues']
        data = {'venues':[]}
        for p in places_list:
            place = place_serializers(p)
            data['venues'].append(place)
        return sz_api_response.Response(data)         