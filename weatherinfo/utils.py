import json
import logging
import requests
from infiweather import settings
from .models import CityWeatherDetails
logging = logging.getLogger(__name__)


def fetch_weather_info():
    endpoint = settings.WEATHER_API_ENDPOINT
    data = open('weatherinfo/city_name.json')
    json_data = json.load(data)
    city_names = json_data["city_names"]
    logging.info("city names {}".format(json_data["city_names"]))

    for city in city_names:
        url = endpoint + "/data/2.5/weather?q={}&appid={}".format(city, settings.WEATHER_API_KEY)
        logging.info("calling Weather api, url  {} ".format(url))
        try:
            r = requests.get(url)
            logging.info("status code {}".format(r.status_code))
            if r.status_code != requests.codes.ok:
                logging.error(
                    "Unsuccessful response from Weather api ERROR = {}".format(r.json()["message"]))
            else:
                data = r.json()
                logging.info("successful response from weather api data - {}".format(data))
                cityWeatherDetails = {
                    "city_name": data["name"],
                    "weather_details": data["weather"],
                    "wind_details": data["wind"],
                    "temperature_details": data["main"],
                    "visibility": data["visibility"],
                    "lat": data["coord"]["lat"],
                    "long": data["coord"]["lon"],
                    "openweather_id": data["id"]
                }
                city_details = CityWeatherDetails.objects.filter(city_name=data["name"])
                if city_details.exists():
                    city_details.update(**cityWeatherDetails)
                else:
                    print("insert")
                    city_details = CityWeatherDetails(**cityWeatherDetails)
                    city_details.save()
        except requests.exceptions.RequestException as e:
            logging.error(
                "Error while calling WEATHER API, City {}, ERROR = {}".format(city, e))
