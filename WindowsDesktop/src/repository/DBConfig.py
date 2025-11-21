from sqlalchemy import create_engine, MetaData
from src.repository.Singleton import SingletonMeta


class DBConfig(metaclass=SingletonMeta):

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.engine = create_engine("sqlite:///src/data/dataBase.db")
            self.metadata = MetaData()
