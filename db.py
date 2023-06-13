import pymysql
import sqlalchemy
import config

from google.cloud.sql.connector import Connector, IPTypes


def getconn() -> pymysql.connections.Connection:
    with Connector() as connector:
        conn = connector.connect(
            config.DB_CONNECTION_NAME,
            "pymysql",
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            db=config.DB_NAME,
            ip_type=IPTypes.PUBLIC,
            enable_iam_auth=False,
        )
    return conn


pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)
