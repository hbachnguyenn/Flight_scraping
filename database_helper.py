from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import inspect
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import os

def pgconnect():
    load_dotenv()
    host        = os.getenv('HOST')
    db_user     = os.getenv('USER')
    db_pw       = os.getenv('PASSWORD')
    default_db  = os.getenv('DATABASE')
    port        = os.getenv('PORT')
    try:
        db = create_engine(f'postgresql+psycopg2://{db_user}:{db_pw}@{host}:{port}/{default_db}', echo=False)
        conn = db.connect()
        print('Connected successfully.')
    except Exception as e:
        print("Unable to connect to the database.")
        print(e)
        db, conn = None, None
    return db,conn

def schema_setup(conn):
    conn.execute(text("""
        CREATE SCHEMA IF NOT EXISTS sgn_syd;
        COMMIT;
    """))
    conn.execute(text("SET search_path TO sgn_syd"))

def inspect_schema(db):
    print(inspect(db).get_schema_names())

def create_flight_table(conn):
    conn.execute(text("""
        DROP TABLE IF EXISTS sgn_syd;
        CREATE TABLE IF NOT EXISTS "sgn_syd" (
            departure VARCHAR(10),
            destination VARCHAR(10),
            price INTEGER,
            brand VARCHAR(3),
            flight_date TIMESTAMP,
            scrape_date TIMESTAMP
        )
    """))

def query(conn, sqlcmd, args=None, df=True):
    result = pd.DataFrame() if df else None
    try:
        if df:
            result = pd.read_sql_query(sqlcmd, conn, params=args)
        else:
            result = conn.execute(text(sqlcmd), args).fetchall()
            result = result[0] if len(result) == 1 else result
    except Exception as e:
        print("Error encountered: ", e, sep='\n')
    return result

def save_data(conn, data: pd.DataFrame):
    data.to_sql(name='sgn_syd', con=conn, if_exists='append', index=False)

