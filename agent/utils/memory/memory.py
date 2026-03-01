from psycopg_pool import AsyncConnectionPool
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("POSTGRES_URL")

pool = AsyncConnectionPool(
    conninfo=DB_URI,
    max_size=10,
    kwargs={"autocommit": True},
    open=False
)