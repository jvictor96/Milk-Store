from sqlmodel import SQLModel, create_engine
from config import settings

# Define your database credentials (replace with your actual info)
DB_USER = settings.database_connection.user
DB_PASSWORD = settings.database_connection.password
DB_HOST = settings.database_connection.host
DB_PORT = settings.database_connection.port
DB_NAME = settings.database_connection.name

# Create the connection URL string
database_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(database_url)
SQLModel.metadata.create_all(engine)
