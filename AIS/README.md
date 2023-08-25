To run this program, you will first need to **create the SQL data base**. Therefore, the **_dataExtractor.py_** needs to be runned.
In the `main` function, the specific data base needed must be select or uncomment to be added, then to query the data:
```
    # Add data to db
    # add_data_to_db(conn, 'nari_static.csv', 'ais_data_static')
    # add_data_to_db(conn, 'nari_dynamic.csv', 'ais_data_dynamic')
    # add_data_to_db(conn, 'AIS 2009.csv', 'ais_data_2009')

    # Query the data
    # mmsi = 227635210
    # query_data_2009(conn, 'ais_data_2009', mmsi)

    mmsi = 227443000
    query_data_dynamic(conn, 'ais_data_dynamic', mmsi)
```
