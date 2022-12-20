from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import Session
from sqlalchemy_json import MutableJson, NestedMutableJson, mutable_json_type

from src.config import DB_NAME, GLOBAL_DATA_TABLE, KEYBINDS_TABLE, KEYMAPS_TABLE
from src.services.logging.setup_logger import create_exception_log, logger


def start_connect_to_db():
    """
        Create db connection, if smth went wrong raise the error and leave
        :raise: a problem to connect with db
    :return:
    """
    try:
        engine = create_engine(DB_NAME)
        connect = engine.connect()
        connect.close()
        return engine

    except:
        logger.exception('Connection to db error')
        create_exception_log()
        quit()


engine = start_connect_to_db()
Base = declarative_base()


class Keymaps(Base):
    """
        Table with all keybinds
    """

    __tablename__ = KEYMAPS_TABLE

    id = Column(Integer,
                primary_key=True)
    title_id = Column(Integer,
                      comment='title of keybind')


class Keybinds(Base):
    """
        Table with all keybinds
    """

    __tablename__ = KEYBINDS_TABLE

    id = Column(Integer,
                primary_key=True)
    keymap = Column(Integer, 
                    ForeignKey('keymaps.id'),
                    comment='bind for this keymap')
    keybind = Column(String(16),
                     comment='keybind for this keymap')
    amount_use = Column(Integer,
                        comment='amount use this keybind, (if setup to count keybinds)',
                        default=0)


class GlobalData(Base):
    """
        Data which needed to store something settings and other which save the user
    """
    __tablename__ = GLOBAL_DATA_TABLE

    id = Column(Integer,
                primary_key=True)
    data = Column(NestedMutableJson,
                  comment='saved user data')


def create_db_tables():
    """
        Create all tables, if it not exists
    """
    Base.metadata.create_all(engine)


create_db_tables()
session = Session(bind=engine)

