# -*- coding: utf-8 -*-
from django import forms
from sz import settings
from sz.core import models

class PlaceExploreRequestForm(forms.Form):
    latitude = forms.FloatField(
    	required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(
    	required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')
    query = forms.CharField(required=False, label=u'Запрос')
    radius = forms.IntegerField(
        required=True, min_value=0, max_value=5000,
        label=u'Удалённость', initial=settings.BLOCKS_RADIUS)

class PlaceSearchRequestForm(forms.Form):
    latitude = forms.FloatField(
        required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(
        required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')
    query = forms.CharField(required=False, label=u'Запрос')
    radius = forms.IntegerField(
        required=False, min_value=0, max_value=5000,
        label=u'Удалённость', initial=settings.BLOCKS_RADIUS)

class PaginatedRequestForm(forms.Form):
    max_id = forms.IntegerField(required=False, min_value=0)
    limit = forms.IntegerField(required=False, min_value=1, max_value=50, initial=settings.DEFAULT_PAGINATE_BY)
    offset = forms.IntegerField(required=False, min_value=0)


class MessageRequestForm(PaginatedRequestForm):
    query = forms.CharField(required=False, label=u'Запрос')
    category = forms.ModelChoiceField(
        queryset=models.Category.objects.all(), required=False, label=u'Категория')
    photo = forms.BooleanField(label=u'Только с фото', required=False)

class NewsRequestForm(MessageRequestForm):
    latitude = forms.FloatField(required=True, min_value=-90.0, max_value=90.0, label=u'Широта')
    longitude = forms.FloatField(required=True, min_value=-180.0, max_value=180.0, label=u'Долгота')
    radius = forms.IntegerField(
        required=False, min_value=0, max_value=5000, label=u'Удалённость', 
        # initial=settings.DEFAULT_RADIUS
        initial=0
        )

