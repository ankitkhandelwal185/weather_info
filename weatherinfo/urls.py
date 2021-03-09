from django.conf.urls import url
from weatherinfo import views


urlpatterns = [
    url("email/weather/info/", views.email_weather_info),
    url("weather/info/", views.get_weather_info),
    url('register/', views.Register),
    url('login/', views.Login),
    url('logout/', views.Logout),
]

