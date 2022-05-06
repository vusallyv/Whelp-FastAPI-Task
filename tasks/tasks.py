from celery import Celery
from celery.utils.log import get_task_logger
from db.models import IPAddress
from db.models import User

celery = Celery('tasks', broker='amqp://user:12345@127.0.0.1:5672//')

celery_log = get_task_logger(__name__)


@celery.task(name="create_task")
def create_task(current_user):
    if current_user and User.filter(User.username == current_user).first():
        current_user_id = User.filter(User.username == current_user).first().id
        from ipdata import ipdata
        ipdata = ipdata.IPData(
            '796e8b385b59fa5289a401c8bcb8ecaca76d79bdf425e45ea8b30c48')
        response = ipdata.lookup(ip='')
        ip_address = IPAddress(
            ip=response["ip"],
            user_id=current_user_id,
            is_eu=response["is_eu"],
            city=response["city"],
            region=response["region"],
            region_code=response["region_code"],
            country_name=response["country_name"],
            country_code=response["country_code"],
            continent_name=response["continent_name"],
            continent_code=response["continent_code"],
            latitude=response["latitude"],
            longitude=response["longitude"],
            postal=response["postal"],
            calling_code=response["calling_code"],
            flag=response["flag"]
        )
        ip_address.save()
        return ip_address
    else:
        return None
