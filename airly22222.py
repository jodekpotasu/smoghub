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

address=input("Bardzo prosze podać kod pocztowy lub adres: ")
geolocator = Nominatim(user_agent="Monika")
location = geolocator.geocode(address)
print(location.address)
print((location.latitude, location.longitude))

LATITUDE = location.latitude
LONGITUDE = location.longitude
MAX_DIST_KM = 0.5


import logging
import sys
from collections import OrderedDict
import asyncio
from pathlib import Path

import aiohttp

from airly import Airly
from airly.measurements import Measurement

try:
    API_KEY = 'nzvM1TYFA3NIR92r8MJ28fYWvbkJyCj1'
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
                weather_dict.append((m, current.values.get(m)))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
PM1z = weather_dict[0]
PM25z= weather_dict[1]
PM10z= weather_dict[2]
TEMPERATUREz= weather_dict[3]
HUMIDITYz= weather_dict[4]
PRESSUREz= weather_dict[5]
pm25H= PM25z[1]
pm10H= PM10z[1]
temperature= TEMPERATUREz[1]
humidity= HUMIDITYz[1]
pressure= PRESSUREz[1]
pm25H = float(pm25H)
pm10H = float(pm10H)
humidity = float(humidity)
pressure = float(pressure)
temperature = float(temperature)
