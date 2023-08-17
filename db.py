import config
import psycopg2
import pymysql


# from google.cloud.sql.connector import Connector, IPTypes
#
#
# def getconn() -> pymysql.connections.Connection:
#     with Connector() as connector:
#         conn = connector.connect(
#             config.DB_CONNECTION_NAME,
#             "pymysql",
#             user=config.DB_USER,
#             password=config.DB_PASSWORD,
#             db=config.DB_NAME,
#             ip_type=IPTypes.PUBLIC,
#             enable_iam_auth=False,
#         )
#     return conn
#

conn = psycopg2.connect(
        host="localhost",
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD)

cur = conn.cursor()

conn.commit()

cur.close()
conn.close()

