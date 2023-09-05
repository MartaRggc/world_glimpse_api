import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

database_user = os.environ.get('DATABASE_USER')
database_host = os.environ.get('DATABASE_HOST')
database_port = os.environ.get('DATABASE_PORT')
database_password = os.environ.get('DATABASE_PASSWORD')
database_name = os.environ.get('DATABASE_NAME')

engine = create_engine(
    f"mysql+mysqlconnector://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}",
    echo=True
)


Session = sessionmaker(bind=engine)

session = Session()
