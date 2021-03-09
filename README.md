# city weather information
Prerequisite    
Clone repo and create a virtual env    
install packages from requirements.txt    
create database as mentioned in settings file    
create local_settings.py and update keys 

# Commands
Create virtualenv : virtualenv infienv    
Activate virtualenv : source venv/bin/activate    
git clone   https://github.com/ankitkhandelwal185/weather_info.git    
pip install -r requirements.txt    
python manage.py migrate    
python manage.py runserver    
Celery set up to run Async task which will fetch and update weather info
celery -A infiweather worker -l info    
celery -A infiweather beat -l info


Api to get weather info data as json    
http://localhost:8000/api/weather/info/    

Api to Email weather information as excl    
http://localhost:8000/api/email/weather/info/

Api to register user   
http://localhost:8000/api/register/     

Api to login user     
http://localhost:8000/api/login/    

Api to logout user    
http://localhost:8000/api/logout/
