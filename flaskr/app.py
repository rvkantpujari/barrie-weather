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

    i = 0
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














def dump_code():
    cityName = "Barrie"
    api = os.getenv("OPEN_WEATHER_MAP_API")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={api}"
    
    # 1st API Call
    res = requests.get(url).json()
    name = res['name']
    lon = res['coord']['lon']
    lat = res['coord']['lat']

    exclude = "minutely,daily"
    units = "metric"
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={api}"
    print(url)

    # 2nd API Call
    res = requests.get(url).json()

    # Current Weather Data
    currTemp = [] # Empty list
    currTemp = round(res['current']['temp'])
    currFeelsLike = round(res['current']['feels_like'])
    currWeatherMain = res['current']['weather'][0]['description']
    currHumidity = res['current']['humidity']
    currVisibility = round(res['current']['visibility']/1000, 1)
    icon = res['current']['weather'][0]['icon']
    currTempIcon = f'http://openweathermap.org/img/wn/{icon}.png'

    # Created a dictionary of Current Weather
    current = { 
        'temp' : currTemp, 'feels_like' : currFeelsLike, 
        'weather' : currWeatherMain, 'humidity' : currHumidity,
        'visibility' : currVisibility, 'icon' : currTempIcon
    }

    hrTemp = []; hrHumidity = []; hrVisibility = []; hrWeatherMain = []; hrTempIcon = []
    
    hr = 0
    hourlyTemp = { 
        'temp' : round(res['hourly'][hr]['temp']), 'humidity' : round(res['hourly'][hr]['humidity']), 
        'visibility' : round(res['hourly'][hr]['visibility']), 'weather' : res['hourly'][hr]['weather'][0]['description'], 
        'icon' : res['hourly'][hr]['weather'][0]['icon'], 'datetime' : time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(res['hourly'][hr]['dt']))
    }
    
    # res['hourly'][hr]['dt']
    
    print(hourlyTemp)
    print(current)
        

    """# Created a dictionary of Hourly Weather
    hourlyTemp = { 
        'Temp' : hrTemp, 'Humidity' : hrHumidity, 
        'Visibility' : hrVisibility, 'Weather' : hrWeatherMain, 
        'Icon' : hrTempIcon
    }"""
    

    now = datetime.now()
    s1 = now.strftime("%h %d, %I:%M %p")


    """print(datetime.fromtimestamp(1649307600))
    theDate = time.strftime('%Y-%m-%d', time.localtime(1649307600))
    theTime = time.strftime('%H:%M:%S', time.localtime(1649307600))
    print(time.strftime('%A, %Y-%m-%d %H:%M:%S', time.localtime(1649307600)))
    print(datetime.utcnow())
    print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(1649307600)))
    print(time.strftime("%Y-%m-%d %H:%M:%S', time.localtime(1649307600)))
    """

def demo():
    cityName = "Barrie"
    degSymbol = u'\N{DEGREE SIGN}'
    
    now = datetime.now() # Current Date & Time
    s1 = now.strftime("%h %d, %I:%M %p")

    # ---------------------------------------- Live API ----------------------------------------

    api = os.getenv("OPEN_WEATHER_MAP_API")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={api}"
    
    # 1st API Call
    res = requests.get(url).json()
    name = res['name']
    lon = res['coord']['lon']
    lat = res['coord']['lat']

    exclude = "minutely"
    units = "metric"
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={api}"
    #print(url)

    # 2nd API Call
    res = requests.get(url).json()

    # Current Weather Data
    currTemp = [] # Empty list
    currTemp = round(res['current']['temp'])
    currFeelsLike = round(res['current']['feels_like'])
    currWeatherMain = res['current']['weather'][0]['description']
    currHumidity = res['current']['humidity']
    currVisibility = round(res['current']['visibility']/1000, 1)
    icon = res['current']['weather'][0]['icon']
    currTempIcon = f'http://openweathermap.org/img/wn/{icon}.png'

    # Created a dictionary of Current Weather
    current = { 
        'temp' : currTemp, 'feels_like' : currFeelsLike, 
        'weather' : currWeatherMain, 'humidity' : currHumidity,
        'visibility' : currVisibility, 'icon' : currTempIcon
    }

    # ---------------------------------------- -------- ----------------------------------------

    USER = os.getenv("MONGODB_USER")
    PASS = os.getenv("MONGODB_PASS")

    client = MongoClient(f"mongodb+srv://{USER}:{PASS}@weather.fnjiw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    
    # db & collection
    db = client["weatherDB"]
    hrCollection = db["hourlyWeather"]
    currCollection = db["currentWeather"]

    chartDataRows = []
    
    hrTemp  = []; hrHumidity = []; hrIcons = []; hrTimes = []; hrDates = []; hrWeather = []

    i = 0
    for hrData in hrCollection.find({}, {'_id':0}).sort("created", DESCENDING).limit(48):
        hrTemp.append(hrData['temp'])
        chartDataRows.append(f"createCustomHTMLContent('http://openweathermap.org/img/wn/{hrData['icon']}.png')")
        hrHumidity.append(hrData['humidity'])
        hrTimes.append(datetime.fromtimestamp(hrData['timestamp']).strftime('%I %p'))
        hrDates.append(time.strftime("%h %d, %Y", time.gmtime(hrData['timestamp'])))
        hrIcons.append(hrData['icon'])
        hrWeather.append(hrData['weather'].title())
    
    #print(datetime.fromtimestamp(1649635200).strftime('%I %p'))
    
    hrTemp.reverse(); hrHumidity.reverse(); hrTimes.reverse(); hrDates.reverse(); hrIcons.reverse(); hrWeather.reverse()

    currData = currCollection.find({}, {'_id':0}).sort("created", DESCENDING).limit(1)

    currData = currCollection.find_one(sort=[("timestamp", DESCENDING)])
    currData['visibility'] = int(currData['visibility'])/1000
    
    return render_template('index.html', city=name, degSymbol=degSymbol, datetime=s1, current=currData, 
    hrIcons=hrIcons, hrTemp=json.dumps(hrTemp), hrHumidity=hrHumidity, hrTime=hrTimes, hrDates=hrDates, hrWeather=hrWeather)