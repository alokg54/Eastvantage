# Copyright (c) 2023 ...
# All rights reserved
"""
Module Name: ***db_utils***
Author: ***Alok Kumar Gupta***
Email: ***alokg54@gmail.com***
=============================================
This module performs various operation on DB for Eastvantage.
"""

import os
import math
import sqlite3
import pandas as pd
from sqlite3 import Error
from pathlib import Path
from Eastvantage.models import calculate_distance
from Eastvantage.config import NameConstants as NC
from Eastvantage.config import CommonConfig as CC
from Eastvantage.config import AddressesConfig as AC
from Eastvantage import log_util

log = log_util.configure_logger()


def check_create_folder(folder_path):
    """
    Method to check and create the input folder path
    """
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as exp:
        log.error(f'Failed to create {folder_path} - {exp}')
        return False


def create_connection(db_file=CC.ADDRESSES_DB):
    """
    create a database connection to a SQLite database
    """
    try:
        folder_check = check_create_folder(f'{CC.BASE_PATH}{os.sep}{CC.DB_FOLDER}')
        if folder_check:
            conn = sqlite3.connect(db_file)
            log.info("Connection established ...")
            log.info(sqlite3.version)
            return conn
        else:
            log.info('There is an issue creating DB folder.')
    except Error as e:
        log.info(e)


def create_table(table_name, create_table_query):
    """
       create a table in DB
    """
    conn = None
    try:
        conn = create_connection()
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        # Doping table if already exists.
        cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")
        # Creating table
        cursor.execute(create_table_query)
        log.info(f"Table created successfully...")
        log.info(f"Table Name : {table_name}")
        # Commit changes in the database
        conn.commit()
    except Error as e:
        log.info(e)
    finally:
        if conn:
            # Closing the connection
            conn.close()
            log.info("Connection closed successfully")


def insert_into_table(name, address, city, state, zip_code, lat, lon):
    """
    Method to insert data into Database
    """
    try:
        conn = sqlite3.connect(CC.ADDRESSES_DB)
        log.info("Opened database successfully")
        conn.execute(AC.insert_data_query, (name, address, city, state, zip_code, lat, lon))
        log.info("Data inserted successfully...")
        # Commit your changes in the database
        conn.commit()
        # Closing the connection
        conn.close()
        log.info("Connection closed successfully")
    except Exception as exp:
        log.error('Error occurred while inserting data into qatar_auto_txn_release table.')
        raise exp


def delete_from_table(address_id):
    """
    Function to delete row from settlement table based on reference string provided and query passed
    """
    try:
        conn = sqlite3.connect(CC.ADDRESSES_DB)
        log.info("Opened database successfully")
        cursor = conn.cursor()
        log.info(f"Deleting address of ID : {address_id}")
        cursor.execute(AC.delete_query, (address_id,))
        conn.commit()
        log.info("Data deleted from table.")
        cursor.close()
        return True
    except Exception as exp:
        raise exp


def get_lat_lon(address_id):
    """
    Method to get latitude and longitude of an address
    """
    try:
        conn = sqlite3.connect(CC.ADDRESSES_DB)
        log.info("Opened database successfully")
        cursor = conn.cursor()
        log.info("Fetching data from database...")
        cursor.execute(AC.get_data_query, (address_id,))
        fetched_data = cursor.fetchall()
        lat_lon_tup = (fetched_data[0][-2], fetched_data[0][-1])
        # Closing the connection
        conn.close()
        return lat_lon_tup
    except Exception as exp:
        raise exp


def get_all_data():
    """
    Method to get latitude and longitude of an address
    """
    try:
        conn = sqlite3.connect(CC.ADDRESSES_DB)
        log.info("Opened database successfully")
        cursor = conn.cursor()
        log.info("Fetching data from database...")
        cursor.execute(AC.get_all_data_query)
        fetched_data = cursor.fetchall()
        fetched_df = pd.DataFrame(fetched_data)
        log.info('Record fetched.')
        # rename columns names
        if fetched_df.shape[0] > 0:
            fetched_df.columns = AC.COLUMNS
        # Closing the connection
        conn.close()
        return fetched_df
    except Exception as exp:
        raise exp


def get_addresses(lat, lon, distance):
    try:
        # fetching all data from DB
        df = get_all_data()
        origin = (lat, lon)
        df[NC.DISTANCE] = ''
        # iterating locations and calculating the distance then updating it in dataframe
        for index, row in df.iterrows():
            destination = (row[NC.LATITUDE], row[NC.LONGITUDE])
            dist = calculate_distance(origin, destination)
            dist = math.floor(dist * 10) / 10
            df.loc[index, NC.DISTANCE] = dist
        log.info(f'All nearby addresses fetched...')
        requested_df = df[df[NC.DISTANCE] <= int(distance)]
        json_data = requested_df.to_dict(orient='records')
        return json_data
    except Exception as exp:
        log.error(f'Error occurred while generating locations - {exp}')


if __name__ == '__main__':
    # create_table(AC.TABLE_NAME, AC.create_table_query)
    # insert_into_table('Jyoti', 'Barka Gaon', 'Bhabua', 'Bihar', '821108', '52.12345', '16.12345')
    # delete_from_table(1)
    # get_lat_lon(5)
    get_addresses(13.01870506723007, 77.72652840603726, 100)
