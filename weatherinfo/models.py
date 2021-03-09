from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class CityWeatherDetails(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    city_name = models.CharField(max_length=200, blank=True, null=True)
    weather_details = JSONField(blank=True, default=dict)
    wind_details = JSONField(blank=True, default=dict)
    temperature_details = JSONField(blank=True, default=dict)
    visibility = models.IntegerField()
    lat = models.CharField(max_length=20, blank=True, null=True)
    long = models.CharField(max_length=20, blank=True, null=True)
    openweather_id = models.IntegerField()