import database_helper

def database_setup():
    db, conn = database_helper.pgconnect()
    if db and conn:
        database_helper.schema_setup(conn)
        database_helper.inspect_schema(db)
        database_helper.create_flight_table(conn)



def main():
    database_setup()

    pass

if __name__ == "__main__":
    main()