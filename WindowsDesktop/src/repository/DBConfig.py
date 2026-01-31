from sqlalchemy import create_engine, MetaData


class DBConfig:

    def __init__(self):
        self.engine = create_engine("sqlite:///src/data/dataBase.db")
        self.metadata = MetaData()
