import os

import sqlalchemy as db

from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

load_dotenv()

DATABASE = str(os.getenv('NAME_DB'))
USER = str(os.getenv('USER'))
PASSWORD = str(os.getenv('PASSWORD'))
HOST = str(os.getenv('HOST'))
PORT = str(os.getenv('PORT'))

# Соединение с бд
engine = db.create_engine(
    f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}', echo=True
)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)
