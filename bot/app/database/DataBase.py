from sqlalchemy import create_engine

from configuration import config

conf = config.postgres

class DataBase:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{conf.username}:{conf.userpassword}@{conf.host}:{conf.port}/{conf.database}"
        )