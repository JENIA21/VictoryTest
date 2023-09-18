from dotenv import dotenv_values
from peewee import *
from playhouse.migrate import PostgresqlMigrator

env_vars = dotenv_values('.env')

db = PostgresqlDatabase(
    env_vars['DB_NAME'],
    user=env_vars['DB_USER'],
    password=env_vars['DB_PASSWORD'],
    host=env_vars['DB_HOST'])

migrator = PostgresqlMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db


class DataUser(BaseModel):
    id = PrimaryKeyField(null=False)
    chat_id = IntegerField(null=True)
    message = CharField(null=True)
    video_mess = CharField(null=True)
    img_mess = CharField(null=True)

    class Meta:
        db_table = "data_user"


db.connect()
DataUser.create_table()
