from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = 'sqlite:///db.sqlite3'

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker()
Base = declarative_base()
