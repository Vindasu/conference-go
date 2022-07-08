from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": f"{city} {state}"}
    res = requests.get(url, params=params, headers=headers)
    the_json = res.json()
    picture_dict = {"picture_url": the_json["photos"][0]["src"]["original"]}
    return picture_dict


def get_lat_lon(city, state):
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {"appid": OPEN_WEATHER_API_KEY, "q": f"{city},{state},USA"}
    res = requests.get(geo_url, params=geo_params)
    the_json = res.json()
    lat = the_json[0]["lat"]
    lon = the_json[0]["lon"]
    return lat, lon


def get_weather_data(city, state):
    # Use the Open Weather API
    lat, lon = get_lat_lon(city, state)
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "appid": OPEN_WEATHER_API_KEY,
        "lat": lat,
        "lon": lon,
        "units": "imperial",
    }
    res = requests.get(weather_url, params=weather_params)
    the_json = res.json()
    weather = {
        "temp": the_json["main"]["temp"],
        "description": the_json["weather"][0]["description"],
    }
    return weather
