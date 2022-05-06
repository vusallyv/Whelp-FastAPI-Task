from fastapi import HTTPException
from db.models import IPAddress


def create_ip_address(response):
    ip_address = IPAddress(
        ip=response["ip"],
        user_id=1,
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


def get_status_of_task(ip_address_id):
    ip_address = IPAddress.filter(IPAddress.id == ip_address_id).first()
    if ip_address:
        return ip_address
    return HTTPException(status_code=404, detail="IP Address not found")
