# Copyright (c) 2023 ...
# All rights reserved
"""
Module Name: **config**
Author: ***Alok Kumar Gupta***
Email: ***alokg54@gmail.com***
=============================================
Module to have configuration related to Eastvantage
"""

import os
from datetime import date


class CommonConfig:
    BASE_PATH = f'{os.getcwd()}'
    DB_FOLDER = 'DB'
    today = date.today()
    today_date = today.strftime("%d-%b-%Y")
    ADDRESSES_DB = f"{BASE_PATH}{os.sep}{DB_FOLDER}{os.sep}address_details.db"


class AddressesConfig:
    TABLE_NAME = 'address'
    COLUMNS = ['id', 'name', 'address', 'city', 'state', 'zipcode', 'latitude', 'longitude']
    create_table_query = f""" CREATE TABLE IF NOT EXISTS address (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                address TEXT NOT NULL,
                                city TEXT NOT NULL,
                                state TEXT NOT NULL,
                                zipcode TEXT NOT NULL,
                                latitude REAL NOT NULL,
                                longitude REAL NOT NULL
                                ) """
    insert_data_query = f"""INSERT INTO address 
                                (name, address, city, state, zipcode, latitude, longitude) 
                                VALUES (?, ?, ?, ?, ?, ?, ?);"""
    update_query = "UPDATE address SET name = ?, address = ?, city = ? , state = ?, zipcode = ?, latitude = ?, " \
                   "longitude = ? WHERE id = ?"
    delete_query = """DELETE FROM address WHERE id = (?);"""
    get_data_query = """SELECT * FROM address WHERE id = (?);"""
    get_all_data_query = """SELECT * FROM address;"""


class NameConstants:
    DISTANCE = 'distance'
    LATITUDE = 'latitude'
    LONGITUDE = 'longitude'

