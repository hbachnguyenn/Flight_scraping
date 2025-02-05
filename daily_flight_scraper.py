from datetime import datetime
import nodriver as uc
import database_helper
import scrape_helper
import helper
import asyncio
import sqlalchemy
from sqlalchemy import text

def setup_database():
    db, conn = database_helper.pgconnect()
    if db and conn:
        database_helper.schema_setup(conn)
        database_helper.inspect_schema(db)
        database_helper.create_flight_table(conn)
    return db, conn

def main():
    db, conn = setup_database()
    page = asyncio.get_event_loop().run_until_complete(scrape_helper.load_driver_and_page())
    page = asyncio.get_event_loop().run_until_complete(scrape_helper.fill_in_data(page, datetime.now()))
    data = asyncio.get_event_loop().run_until_complete(scrape_helper.scrape_data_30_days(page))
    database_helper.save_data(conn, data)

    print('----------------------------------------------')
    print(database_helper.query(conn, 'select * from sgn_syd'))
    pass

if __name__ == "__main__":
    main()