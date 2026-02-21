from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
import os
from dotenv import load_dotenv
load_dotenv()

DB_URI  =  os.getenv("POSTGRES_URL")
pool = ConnectionPool(
    conninfo=DB_URI,
    max_size=10,
    kwargs={"autocommit": True}
)
checkpointer = PostgresSaver(pool)
checkpointer.setup()