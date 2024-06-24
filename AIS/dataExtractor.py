import sqlite3
import pandas as pd
import math

def add_data_to_db(conn, filename, tablename):
    chunksize = 50000 # Adjust this value based on available memory

    if filename == 'AIS 2009.csv':
        chunk_generator = pd.read_csv(filename, sep = ';', chunksize=chunksize)

    else:
        chunk_generator = pd.read_csv(filename, chunksize=chunksize)

    for chunk in chunk_generator:
        chunk.to_sql(tablename, conn, if_exists='append', index=False)


def query_data_static(conn, tablename, mmsi):
    query = f'SELECT * FROM {tablename} WHERE sourcemmsi = {mmsi}'
    df_mmsi = pd.read_sql_query(query, conn)
    print(df_mmsi)

# def query_data_2009(conn, tablename, mmsi):
#     query = f'SELECT * FROM {tablename} WHERE MMSI_Number = {mmsi}'
#     df_mmsi = pd.read_sql_query(query, conn)
#     print(df_mmsi)

def query_data_2009(conn, tablename, mmsi):
    query = f'SELECT * FROM {tablename} WHERE MMSI_Number = {mmsi}'
    df_mmsi = pd.read_sql_query(query, conn)

    # # Convert Latitude and Longitude to radians
    # df_mmsi['Latitude'] = df_mmsi['Latitude'].apply(math.radians)
    # df_mmsi['Longitude'] = df_mmsi['Longitude'].apply(math.radians)

    # Get center points
    center_latitude = df_mmsi['Latitude'].mean()
    center_longitude = df_mmsi['Longitude'].mean()

    # Centralize coordinates
    df_mmsi['Latitude'] -= center_latitude
    df_mmsi['Longitude'] -= center_longitude

    # # Convert to kilometers
    df_mmsi['Latitude'] *= 100
    df_mmsi['Longitude'] *= 100 * math.cos(center_latitude)

    # Convert heading to radians
    df_mmsi['Heading'] = df_mmsi['Heading'].apply(math.radians)

    # Compute average speed
    average_speed = df_mmsi['Speed'].mean()

    # Scale speeds with respect to the average speed
    df_mmsi['Speed'] = df_mmsi['Speed'].apply(lambda x: x / average_speed if average_speed != 0 else 0)

    print(df_mmsi)

    return df_mmsi

def query_data_dynamic(conn, tablename, mmsi):
    query = f'SELECT * FROM {tablename} WHERE sourcemmsi = {mmsi}'
    df_mmsi = pd.read_sql_query(query, conn)

    # Get center points
    center_latitude = df_mmsi['lat'].mean()
    center_longitude = df_mmsi['lon'].mean()

    # Centralize coordinates
    df_mmsi['lat'] -= center_latitude
    df_mmsi['lon'] -= center_longitude

    # Convert heading to radians
    df_mmsi['trueheading'] = df_mmsi['trueheading'].apply(math.radians)

    # Compute average speed
    average_speed = df_mmsi['speedoverground'].mean()

    # Scale speeds with respect to the average speed
    df_mmsi['speedoverground'] = df_mmsi['speedoverground'].apply(lambda x: x / average_speed if average_speed != 0 else 0)

    df_mmsi['speedoverground'] /= 10

    print(df_mmsi)

    return df_mmsi

# def query_data_dynamic(conn, tablename, mmsi):
#     query = f'SELECT * FROM {tablename} WHERE sourcemmsi = {mmsi}'
#     df_mmsi = pd.read_sql_query(query, conn)
#     print(df_mmsi)

#     return df_mmsi


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
    # mmsi = 227635210
    # query_data_2009(conn, 'ais_data_2009', mmsi)

    mmsi = 227443000
    query_data_dynamic(conn, 'ais_data_dynamic', mmsi)

    conn.close()

if __name__ == "__main__":
    main()


