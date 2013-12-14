# -*- coding: utf-8 -*-
from rest_framework import permissions, status

from sz.api import serializers
from sz.api.response import Response as sz_api_response
from sz.api.serializers import AuthUserSerializer, \
    RegistrationSerializer, ResendingConfirmationKeySerializer
from sz.api.views import SzApiView


class UsersRoot(SzApiView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            user_serializer = AuthUserSerializer(instance=user)
            return sz_api_response(user_serializer.data)
        return sz_api_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from sz.core.models import RegistrationProfile
class UsersRootResendingActivationKey(SzApiView):
    """ Sends an email with a confirmation key """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ResendingConfirmationKeySerializer(
            data=request.DATA
        )
        if serializer.is_valid():            
            return sz_api_response({})
            #Next strings - for testing
            # try:
            #     key = RegistrationProfile.objects.get(user__email=request.DATA[u"email"]).activation_key
            # except:
            #     key = 'No Key'
            # return sz_api_response({'key':key})
        return sz_api_response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class UserInstanceSelf(SzApiView):
    """ Retrieve profile information for the action user """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        serializer = serializers.UserSerializer(instance=user)
        return sz_api_response(serializer.data)