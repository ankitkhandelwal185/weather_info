from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response

from weatherinfo.helpers import validate_email, send_email
from weatherinfo.models import CityWeatherDetails
from django.core.serializers import serialize
from .serializers import RegisterSerializer

import logging
import json
import pandas as pd

logging = logging.getLogger(__name__)


# API to get Weather info
@api_view(['GET'])
def get_weather_info(request):
    try:
        cityWeatherDetails = CityWeatherDetails.objects.all().order_by('-id')[:30]
        # convert queryset to json data
        json_data = json.loads(serialize('json', cityWeatherDetails))
    except Exception as e:
        logging.error("Exception {}", e)
        return Response("Exception {}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(json_data, status=status.HTTP_200_OK)


# API to email Weather info
@api_view(['POST'])
def email_weather_info(request):
    try:
        logging.info("email_weather_info: request data {}".format(request.data))
        emails = request.data["emails"]
        if emails:
            # check emails if valid or not
            valid_emails = validate_email(emails)
            if valid_emails:
                logging.info("email_weather_info: valid emails {}".format(valid_emails))
                cityWeatherDetails = CityWeatherDetails.objects.all().order_by('-id')[:30]
                # json_data = CityWeatherDetailsSerializer("json", list(cityWeatherDetails.values()), many=True)
                # convert queryset to json data
                json_data = json.loads(serialize('json', cityWeatherDetails))
                pd.DataFrame(json_data).to_excel('output.xlsx', header=False, index=False)
                # call send email method
                send_email(valid_emails)
            else:
                return Response({"msg": "no valid emails"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error("email_weather_info: Exception {}".format(e))
        return Response("email_weather_info: Exception {}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(valid_emails, status=status.HTTP_200_OK)


# Register API
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def Register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token, created = Token.objects.get_or_create(user=user)
    data = {
        "token": token.key
    }
    return Response(data=data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def Login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def Logout(request):
        """
        Calls Django logout method; Does not work for UserTokenAuth.
        """
        logout(request)
        return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)




