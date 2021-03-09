from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from weatherinfo.utils import fetch_weather_info


logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/30')),
    name="task_latest_weather_info",
    ignore_result=True
)
def task_save_latest_weather_info():
    """
    Saves latest weather info
    """
    fetch_weather_info()
    logger.info("Saved latest weather info")