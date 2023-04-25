# Copyright (c) 2023 ...
# All rights reserved
"""
Module Name: **main**
==============================
Main module exposes all the restapi methods available
"""

import uvicorn
import math
from Eastvantage import db_utils
from Eastvantage.models import AddressUpdate, validate_address, calculate_distance
from fastapi import FastAPI
from Eastvantage.config import AddressesConfig
from Eastvantage import log_util
log = log_util.configure_logger()

app = FastAPI()


@app.get("/")
def root():
    try:
        _version_text = '1.0.0'
        return {"message": f"Welcome to Eastvantage addresses database, Version: {_version_text} "}
    except Exception as exp:
        log.error(f'Error Occurred while returning root data - {exp}')


@app.post("/address/create-address")
def create_address(name, address, city, state, zipcode, latitude, longitude):
    """
        Create an address field and insert into database.
    """
    try:
        db_utils.insert_into_table(name, address, city, state, zipcode, latitude, longitude)
        return True
    except Exception as exp:
        log.error('Error while inserting address details into database...')
        raise exp


# Update address
@app.put("/address/{address_id}")
def update_address(address_id: int, addresses: AddressUpdate):
    try:
        validate_address(addresses)
        conn = db_utils.create_connection()
        c = conn.cursor()
        c.execute(AddressesConfig.update_query,
                  (addresses.name, addresses.address, addresses.city, addresses.state, addresses.zipcode,
                   addresses.latitude, addresses.longitude, address_id))
        conn.commit()
        conn.close()
        return {"message": "Address updated successfully."}
    except Exception as exp:
        log.error(f'Error occurred while updating address - {exp}')
        raise


@app.delete("/address/delete-address")
def delete_address(address_id):
    """
        Delete an address field from database.
    """
    try:
        db_utils.delete_from_table(address_id)
        return True
    except Exception as exp:
        log.error('Error while deleting data from database...')
        raise exp


@app.get("/address/distance")
def get_distance(address_id1, address_id2):
    """
        Find the distance between two co-ordinates
    """
    try:
        coordinate1 = db_utils.get_lat_lon(address_id1)
        coordinate2 = db_utils.get_lat_lon(address_id2)
        dist = calculate_distance(coordinate1, coordinate2)
        dist = math.floor(dist*10)/10
        return f'{dist} km'
    except Exception as exp:
        log.error(f'Error Occurred while finding the distance - {exp}')


@app.get("/address/addresses")
def get_addresses(origin_latitude, origin_longitude, distance):
    """
        Finding locations nearby
    """
    try:
        adds = db_utils.get_addresses(origin_latitude, origin_longitude, distance)
        return adds
    except Exception as exp:
        log.error(f'Error Occurred while fetching locations - {exp}')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
