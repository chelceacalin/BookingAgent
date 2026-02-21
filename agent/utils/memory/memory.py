from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

DB_URI  = "postgresql://postgres:postgres@localhost:5432/postgres"
pool = ConnectionPool(
    conninfo=DB_URI,
    max_size=10,
    kwargs={"autocommit": True}
)
checkpointer = PostgresSaver(pool)
checkpointer.setup() 