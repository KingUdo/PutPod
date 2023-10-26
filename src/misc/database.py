from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
from .helpers import get_env

Base = declarative_base()
DATABASE_SESSION = sessionmaker()

ENGINE = None


def get_engine():
    # Config
    return create_engine('sqlite:///putpod.db')


def initialize_database():
    """create engine and initialize DATABASE_SESSION so that sessions can be opened"""
    global ENGINE
    ENGINE = get_engine()
    DATABASE_SESSION.configure(bind=ENGINE)


initialize_database()
