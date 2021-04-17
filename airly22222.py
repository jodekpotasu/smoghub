import aiohttp
import pickle
import logging
import sys
from collections import OrderedDict
import asyncio
from pathlib import Path
import wget
import joblib
import sklearn
import requests
import logging
import sys
from collections import OrderedDict
import asyncio
from pathlib import Path
from airly import Airly
from airly.measurements import Measurement
weather_dict = []
from geopy.geocoders import Nominatim

address=input("Prosze podać kod pocztowy lub adres: ")
geolocator = Nominatim(user_agent="Monika")
location = geolocator.geocode(address)
print(location.address)
print((location.latitude, location.longitude))

# Before running the sample,
#   you need to create .api_key file filled with your API key.
# After you are logged in, you can copy it from here:
#   https://developer.airly.eu/api
try:
    API_KEY = 'HC4lj4KL2cnNmKpLgANyYFdmTaa2GVAB'

except FileNotFoundError:
    print('Save your API key in samples/.api_key file', file=sys.stderr)
    exit(1)

LATITUDE = location.latitude
LONGITUDE = location.longitude
MAX_DIST_KM = 0.5


async def main():
    pyairly_logger = logging.getLogger('pyairly')
    pyairly_logger.setLevel(logging.DEBUG)
    pyairly_logger.addHandler(logging.StreamHandler(sys.stdout))
    async with aiohttp.ClientSession() as http_session:
        airly = Airly(API_KEY, http_session)

        print('\nInstallations {:.2f} km apart from latitude {:f} and '
              'longitude {:f}:\n'
              .format(MAX_DIST_KM, LATITUDE, LONGITUDE))
        sys.stdout.flush()
        installations_list = await airly.load_installation_nearest(
            LATITUDE, LONGITUDE, max_distance_km=MAX_DIST_KM, max_results=-1)
        sys.stdout.flush()
        for i in installations_list:
            print("{}, {}.\n{}: {}\n".format(
                i.address.displayAddress1, i.address.displayAddress2,
                i.sponsor.description, i.sponsor.name))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# loop.close()

import logging
import sys
from collections import OrderedDict
import asyncio
from pathlib import Path

import aiohttp

from airly import Airly
from airly.measurements import Measurement

# Before running the sample,
#   you need to create .api_key file filled with your API key.
# After you are logged in, you can copy it from here:
#   https://developer.airly.eu/api
try:
    API_KEY = 'HC4lj4KL2cnNmKpLgANyYFdmTaa2GVAB'
except FileNotFoundError:
    print('Save your API key in samples/.api_key file', file=sys.stderr)
    exit(1)




async def main():
    pyairly_logger = logging.getLogger('pyairly')
    pyairly_logger.setLevel(logging.DEBUG)
    pyairly_logger.addHandler(logging.StreamHandler(sys.stdout))
    async with aiohttp.ClientSession() as http_session:
        airly = Airly(API_KEY, http_session)
        measurements_clients = OrderedDict([
            ('for nearest installation',
                airly.create_measurements_session_nearest(
                    LATITUDE, LONGITUDE)),
        ])

        for description, client in measurements_clients.items():
            print()
            sys.stdout.flush()
            await client.update()
            sys.stdout.flush()
            current = client.current
            print("Measurements %s:" % description)
            for m in Measurement.MEASUREMENTS_TYPES:
                print("%s: %s" % (m, current.values.get(m)))
                weather_dict.append("%s: %s" % (m, current.values.get(m)))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

print(weather_dict)