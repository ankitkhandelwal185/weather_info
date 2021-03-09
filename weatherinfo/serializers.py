from rest_framework import serializers
from django.contrib.auth.models import User


# City Weather Details Serializer
class CityWeatherDetailsSerializer(serializers.Serializer):
    city_name = serializers.CharField(max_length=200, allow_null=True)
    weather_details = serializers.JSONField(allow_null=True, default=list, required=False)
    wind_details = serializers.JSONField(allow_null=True, default=dict, required=False)
    temperature_details = serializers.JSONField(allow_null=True, default=dict, required=False)
    visibility = serializers.IntegerField(required=False)
    lat = serializers.CharField(max_length=20, allow_null=True)
    long = serializers.CharField(max_length=20, allow_null=True)
    openweather_id = serializers.IntegerField(required=False)


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
                validated_data['username'],
                validated_data['email'],
                validated_data['password']
        )
        return user

