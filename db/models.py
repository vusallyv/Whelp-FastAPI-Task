from peewee import Model, CharField, ForeignKeyField, IntegerField, BooleanField, ForeignKeyField
from db.database import db


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db


class User(BaseModel):
    username = CharField()
    email = CharField()
    password = CharField()


class IPAddress(BaseModel):
    ip = CharField(20)
    user_id = IntegerField, ForeignKeyField('users.id', null=True)
    is_eu = BooleanField(default=False)
    city = CharField(120, null=True)
    region = CharField(120, null=True)
    region_code = CharField(120, null=True)
    country_name = CharField(120, null=True)
    country_code = CharField(120, null=True)
    continent_name = CharField(120, null=True)
    continent_code = CharField(120, null=True)
    latitude = CharField(120, null=True)
    longitude = CharField(120, null=True)
    postal = CharField(120, null=True)
    calling_code = CharField(120, null=True)
    flag = CharField(120, null=True)
