from flask import Flask, render_template, json
from pymongo import MongoClient, DESCENDING

from dotenv import load_dotenv
from datetime import datetime
import requests
import pytz
import time
import os
import sys


load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    cityName = "Barrie"
    degSymbol = u'\N{DEGREE SIGN}'
    new_timezone = pytz.timezone("Canada/Eastern")
    
    now = datetime.now() # Current Date & Time
    now = now.astimezone(new_timezone)
    s1 = now.strftime("%h %d, %I:%M %p")

    USER = os.getenv("MONGODB_USER")
    PASS = os.getenv("MONGODB_PASS")
    
    client = MongoClient(f"mongodb+srv://{USER}:{PASS}@weather.fnjiw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    # db & collection
    db = client["weatherDB"]
    hrCollection = db["hourlyWeather"]
    currCollection = db["currentWeather"]

    chartDataRows = []
    
    hrTemp  = []; hrHumidity = []; hrIcons = []; hrTimes = []; hrDates = []; hrWeather = []

    for hrData in hrCollection.find({}, {'_id':0}).sort("created", DESCENDING).limit(47):
        hrTemp.append(hrData['temp'])
        chartDataRows.append(f"createCustomHTMLContent('http://openweathermap.org/img/wn/{hrData['icon']}.png')")
        hrHumidity.append(hrData['humidity'])
        
        t = datetime.fromtimestamp(hrData['timestamp']).astimezone(new_timezone).strftime('%I %p')
        hrTimes.append(t)
        
        hrDates.append(time.strftime("%h %d, %Y", time.gmtime(hrData['timestamp'])))
        hrIcons.append(hrData['icon'])
        hrWeather.append(hrData['weather'].title())
    

    hrTemp.reverse(); hrHumidity.reverse(); hrTimes.reverse(); hrDates.reverse(); hrIcons.reverse(); hrWeather.reverse()

    currData = currCollection.find({}, {'_id':0}).sort("created", DESCENDING).limit(1)

    currData = currCollection.find_one(sort=[("timestamp", DESCENDING)])
    currData['visibility'] = int(currData['visibility'])/1000
    
    return render_template('index.html', city=cityName, degSymbol=degSymbol, datetime=s1, current=currData, 
    hrIcons=hrIcons, hrTemp=json.dumps(hrTemp), hrHumidity=hrHumidity, hrTime=hrTimes, hrDates=hrDates, hrWeather=hrWeather)


if __name__ == "__main__":
    app.run()