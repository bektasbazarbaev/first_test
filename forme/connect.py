import psycopg2
from config import conf
def connec():
    return psycopg2.connect(**conf)