from playhouse.postgres_ext import PostgresqlExtDatabase, Model
from config import config

db_client = PostgresqlExtDatabase(
    config["db"].get("DATABASE_NAME", "mental_db"),
    user=config["db"].get("USER", "mental_user"),
    password=config["db"].get("PASSWORD", "password"),
    host=config["db"].get("HOST", "localhost"),
    port=config["db"].get("PORT", 5432),
)

class BaseModel(Model):
    class Meta:
        database = db_client
