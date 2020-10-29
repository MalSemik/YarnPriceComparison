from peewee import *

db = SqliteDatabase('yarn.db')

class Yarn(Model):
    name = CharField()
    price = FloatField()
    availability = BooleanField()
    number = CharField()
    page = CharField()
    url = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([Yarn])
