from decouple import config
from playhouse.postgres_ext import PostgresqlExtDatabase, Model

db_client = PostgresqlExtDatabase(
    config("DB_NAME"),
    user=config("DB_USER"),
    password=config("DB_PASSWORD"),
    host=config("DB_HOST"),
    port=config("DB_PORT"),
    autorollback=True
)

class BaseModel(Model):
    class Meta:
        database = db_client
