import requests
import json
import os
from datetime import datetime


class WeatherService:
    def __init__(self):
        self.API_KEY = "04463f871aeb19886d950dc087beb890" 
        self.CITY_NAME = "Jakarta"
        self.LOG_PATH = "log/data_weather.json"


    def getWeatherData(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY_NAME}&appid={self.API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                
                weather_result = {
                    "temperature": temp,
                    "humidity": humidity,
                    "timestamp": timestamp
                }
                
                self.saveToJson(weather_result)
                
                print(f"({timestamp} GMT+7) Success Running Sampling Data Weather with Result "
                      f"Temperature {temp} °C & Humidity {humidity} %")
                return True
            else:
                error_msg = response.json().get("message", "Unknown Error")
                print(f"({timestamp} GMT+7) - Failed Running Sampling Data Weather with "
                      f"Status Code {response.status_code} - {error_msg}")
                return False
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return False


    def saveToJson(self, data):
        if not os.path.exists("log"):
            os.makedirs("log")
            
        with open(self.LOG_PATH, "w") as f:
            json.dump(data, f, indent=4)