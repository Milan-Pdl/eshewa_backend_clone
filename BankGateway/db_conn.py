from pathlib import Path
import json
config_path="D:\project\eshewa_backend\config.json"
from dataclasses import dataclass
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker,declarative_base
# designing using skeleton pattern, only one object last through out the project for database connection
# @dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus


@staticmethod
def get_db_congiguration(path) -> dict:
    """
    this function returns the database credentials from config file
    *args (path(This takes config file path as a parameter))
    """
    # # yesla absolute path dinxa (resolve la)
    with open(path,"r") as f:
        data=json.loads(f.read())
        return data



class DbConnection:

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DbConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        # Prevent running initialization multiple times
        if self._initialized:
            return

        DbConnection.db_credentials = get_db_congiguration(config_path)

        self.database = DbConnection.db_credentials["BANKDATABASE"]
        self.host = DbConnection.db_credentials["HOST"]
        self.password = quote_plus(DbConnection.db_credentials["PASSWORD"])

        try:
            database_url = f"mysql+pymysql://root:{self.password}@{self.host}:3306/{self.database}"

            self.engine = create_engine(
                database_url,
                pool_pre_ping=True
            )

            self.SessionLocal = sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False
            )

        except Exception as e:
            print("Database connection error:", e)

        DbConnection._initialized = True

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


