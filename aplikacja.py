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


url = 'https://github.com/jodekpotasu/smoghub/blob/master/maps.png?raw=true'
maps = wget.download(url)
from PIL import Image
image = Image.open(maps)
image.show()
import pandas as pd
import wget
import joblib
scaler=joblib.load("scaler.pkl")
print(scaler)
model=joblib.load("gaussianNB.pkl")
print(model)
url = 'https://raw.githubusercontent.com/jodekpotasu/smoghub/master/X_dotestow.csv'
X_dotestowgit = wget.download(url)
X_dotestow = pd.read_csv(X_dotestowgit)
idpunktu = str(input("Proszę podać ID punktu pomiarowego z mapy: "))
temperature = float(input("Proszę podać temperaturę: "))
humidity = float(input("Prosze podać wilgotność w %: "))
pressure = float(input("Prosze podać ciśnienie: "))
pm10H = float(input("Prosze podać PM10 z wczoraj o tej samej godzinie: "))
pm10mean = float(input("Prosze podać średnią PM10 z wczoraj: "))
pm25H = float(input("Prosze podać PM2.5 z wczoraj o tej samej godzinie: "))
pm25mean = float(input("Prosze podać średnią PM2.5 z wczoraj: "))
import requests
import json
from datetime import datetime

import requests, json

humidity = float(humidity)
pressure = float(pressure)
temperature = float(temperature)

X_dotestow['temperature']=temperature
X_dotestow['humidity']=humidity
X_dotestow['pressure']=pressure
X_dotestow['pm10H']=pm10H
X_dotestow['pm25H']=pm25H
X_dotestow['pm10mean']=pm10mean
X_dotestow['pm25mean']=pm25mean
X_dotestow[idpunktu]='1'
x_doskalowania = X_dotestow.iloc[:,:7]

xdf = scaler.transform(x_doskalowania)
xdf = pd.DataFrame(xdf)
xdf.columns = x_doskalowania.columns
xdrugapol=X_dotestow.iloc[:,7:]
xdf=xdf.reset_index(drop=True)
xdrugapol=xdrugapol.reset_index(drop=True)
xkoncowe = pd.concat([xdf, xdrugapol], axis=1)
ykoncowe = model.predict(xkoncowe)
print(ykoncowe)

