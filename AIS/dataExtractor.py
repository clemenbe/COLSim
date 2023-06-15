import sqlite3
import pandas as pd

def add_data_to_db(conn, filename, tablename):
    chunksize = 50000 # Adjust this value based on available memory

    if filename == 'AIS 2009.csv':
        chunk_generator = pd.read_csv(filename, sep = ';', chunksize=chunksize)

    elif filename == 'nari_static.csv':
        chunk_generator = pd.read_csv(filename, chunksize=chunksize)

    for chunk in chunk_generator:
        chunk.to_sql(tablename, conn, if_exists='append', index=False)


def query_data_static(conn, tablename, mmsi):
    query = f'SELECT * FROM {tablename} WHERE sourcemmsi = {mmsi}'
    df_mmsi = pd.read_sql_query(query, conn)
    print(df_mmsi)

def query_data_2009(conn, tablename, mmsi):
    query = f'SELECT * FROM {tablename} WHERE MMSI_Number = {mmsi}'
    df_mmsi = pd.read_sql_query(query, conn)
    print(df_mmsi)

def delete_table(conn, tablename):
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {tablename}")
    conn.commit()


def main():
    conn = sqlite3.connect('ais_database.db')

    # Delete old table
    # delete_table(conn, 'ais_data_2009')

    # Add data to db
    # add_data_to_db(conn, 'nari_static.csv', 'ais_data_static')
    # add_data_to_db(conn, 'nari_dynamic.csv', 'ais_data_dynamic')
    # add_data_to_db(conn, 'AIS 2009.csv', 'ais_data_2009')

    # Query the data
    mmsi = 563238000
    query_data_2009(conn, 'ais_data_2009', mmsi)

    conn.close()

if __name__ == "__main__":
    main()

