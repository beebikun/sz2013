# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.reverse import reverse
from sz.api.views import SzApiView, categorization_service, message_service
from sz.api import serializers, forms
from sz.api import response as sz_api_response
from sz.core import models
from lebowski.api.views import messages as lebowski_messages
from sz.settings import LEBOWSKI_MODE_TEST
"""
Post message - stuff in several stages:
1)An user do POST a message-data on the url "message-preview-list" (MessagePreviewRoot)
2)A client do redirect on "message-preview-publish" (MessagePreviewInstancePublish):
	an user do GET on this url: the server return a processed message-data
3)An user do something with a message-data and
	do POST on "message-previews-publish" (MessagePreviewInstancePublish)


#actually, Dima, this is not very "spoke" titles :/
#so i hope  i understand in right
"""
class MessagePreviewRoot(SzApiView):
    if not LEBOWSKI_MODE_TEST:
        permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user if not LEBOWSKI_MODE_TEST else request.QUERY_PARAMS.get('email')
        previews = models.MessagePreview.objects.filter(user=request.user)
        serializer = serializers.MessagePreviewSerializer(instance=previews)
        return sz_api_response.Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.MessagePreviewSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            message_preview = serializer.object
            message_preview.user = request.user if not LEBOWSKI_MODE_TEST else models.User.objects.get(email=request.DATA.get('email'))
            message_preview.save()
            if message_preview.text is not None:
                if message_preview.text != '':
                    categories = categorization_service.detect_categories(message_preview.text)
                    message_preview.categories.clear()
                    for category in categories:
                        message_preview.categories.add(category)
                #categorization_service.assert_stems(message_preview)
            #dima, what for next 3strings?
            serialized_preview = serializers.MessagePreviewSerializer(instance=message_preview).data
            root_url = reverse('client-index', request=request)
            serialized_preview['photo'] = message_preview.get_photo_absolute_urls(root_url)
            return sz_api_response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessagePreviewInstance(SzApiView):
    """ Retrieve or delete a message preview. """

    def get_object(self, pk):
        try:
            return models.MessagePreview.objects.get(pk=pk)
        except models.MessagePreview.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        message_preview = self.get_object(pk)
        user = request.user if not LEBOWSKI_MODE_TEST else request.QUERY_PARAMS.get('email')
        if message_preview.user != user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.MessagePreviewSerializer(instance=message_preview)
        place_serializer = serializers.PlaceSerializer(instance=message_preview.place)
        data = serializer.data
        root_url = reverse('client-index', request=request)
        data['photo'] = message_preview.get_photo_absolute_urls_and_size(root_url)
        data['place'] = place_serializer.data
        return sz_api_response.Response(data)

    def delete(self, request, pk, format=None):
    	return sz_api_response.Response()
        # message_preview = self.get_object(pk)
        # if message_preview.user != request.user:
        #     return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        # message_preview.delete()
        # return sz_api_response.Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        message_preview = self.get_object(pk)
        user = request.user if not LEBOWSKI_MODE_TEST else request.DATA.get('email')
        if message_preview.user != user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.MessagePreviewSerializer(message_preview, data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return sz_api_response.Response(serializer.data)
        else:
            return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagePreviewInstancePublish(SzApiView):
    """ Publishes a message preview. """

    def get_object(self, pk):
        try:
            return models.MessagePreview.objects.get(pk=pk)
        except models.MessagePreview.DoesNotExist:
            raise Http404
    def get_face(self, pk):
        try:
            return models.Face.objects.get(pk=pk)
        except models.Face.DoesNotExist:
            raise Http404
    def post(self, request, pk, format=None):  
        message_preview = self.get_object(pk) 
        user = request.user if not LEBOWSKI_MODE_TEST else models.User.objects.get(email=request.DATA.get('email'))
        if message_preview.user != user:
            return sz_api_response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.MessagePreviewForPublicationSerializer(
            message_preview, data=request.DATA)        
        if serializer.is_valid():
            face = self.get_face(request.DATA[u'face'])
            photo = message_preview.photo
            if photo:
                faces_list = request.DATA[u'photo'] #??!! не уверена нужно это все перепроверять
                if not faces_list or \
                    not faces_list.get('list') or \
                    not faces_list.get('box') or \
                    not faces_list['box'].get('face'):
                    return sz_api_response.Response(
                                {'faces and box is requered fields'},
                                status=status.HTTP_400_BAD_REQUEST)            
                photo = message_service.unface_photo(
                    faces_list.get('list'),faces_list.get('box'),
                    message_preview)
                if not photo:
                    return sz_api_response.Response(
                        {'faces was not added to photo'},
                        status=status.HTTP_400_BAD_REQUEST)
            serializer.save()       
            message = models.Message(text=message_preview.text, photo=photo,
                                     place=message_preview.place,
                                     face=face, user=message_preview.user)
            message.save()
            for category in message_preview.categories.all():
                message.categories.add(category)
            message_preview.delete()
            categorization_service.assert_stems(message)
            #next string need to change on lebowski answer
            message_serializer = serializers.MessageSerializer(instance=message)
            place_serializer = serializers.PlaceSerializer(instance=message.place)
            user_serializer = serializers.UserSerializer(instance=message.user)
            user_data = dict(
                user_serializer.data,
                **{
                    "latitude":request.DATA.get('latitude',0),
                    "longitude":request.DATA.get('longitude',0)
                    }
                )
            # data = message_serializer.data
            engine_data = lebowski_messages.MessagesCreate().create({
                'message':message_serializer.data,                
                'place':place_serializer.data,
                'creator':user_data
            })
            root_url = reverse('client-index', request=request)
            data = dict(photo=message.get_photo_absolute_urls(root_url), place=place_serializer.data)
            if LEBOWSKI_MODE_TEST:
                data['bl'] = engine_data
            else:            
                data.update(**engine_data)
            print data
            return sz_api_response.Response(data)            
        else:
            return sz_api_response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
