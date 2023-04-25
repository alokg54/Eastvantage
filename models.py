# Copyright (c) 2023 ...
# All rights reserved
"""
Module Name: **models**
==============================
Module to have the all required models
"""

import geopy.distance
from fastapi import HTTPException
from pydantic import BaseModel
from Eastvantage import log_util

log = log_util.configure_logger()


# Address update model
class AddressUpdate(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zipcode: str
    latitude: float
    longitude: float


# Validate address model
def validate_address(address: AddressUpdate):
    if not address.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if not address.address.strip():
        raise HTTPException(status_code=400, detail="Address cannot be empty")

    if not address.city.strip():
        raise HTTPException(status_code=400, detail="City cannot be empty")

    if not address.state.strip():
        raise HTTPException(status_code=400, detail="State cannot be empty")

    if not address.zipcode.strip():
        raise HTTPException(status_code=400, detail="Zipcode cannot be empty")

    if not address.latitude:
        raise HTTPException(status_code=400, detail="Latitude cannot be empty")

    if not address.longitude:
        raise HTTPException(status_code=400, detail="Longitude cannot be empty")


def calculate_distance(origin, destination):
    """
    Method to get the distance between two latitude and longitude
    """
    try:
        dist = geopy.distance.geodesic(origin, destination).km
        log.info(f'distance found - {dist}')
        return dist
    except Exception as exp:
        log.error(f'Error occurred in getting distance - {exp}')


if __name__ == '__main__':
    calculate_distance((47.75127, -117.425781), (12.971599, 77.594566))
