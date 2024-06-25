import os
from langchain_community.utilities import SQLDatabase

db_username = os.environ["POSTGRES_USER"]
db_pwd = os.environ["POSTGRES_PASSWORD"]
db_host = os.environ["POSTGRES_HOST"]
db_port = os.environ["POSTGRES_PORT"]
db_name = os.environ["POSTGRES_DB"]
db_uri = f"postgresql+psycopg2://{db_username}:{db_pwd}@{db_host}:{db_port}/{db_name}"
db = SQLDatabase.from_uri(db_uri)

