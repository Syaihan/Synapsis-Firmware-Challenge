import json
import csv
import os
import random
from datetime import datetime


class MqttHelper:
    def __init__(self, nama_kandidat):
        self.nama_kandidat = nama_kandidat
        self.weather_log = "log/data_weather.json"


    def getSensorData(self):
        """Mengambil data dari JSON soal 2 dan generate data random"""
        try:
            with open(self.weather_log, "r") as f:
                weather = json.load(f)
        except:
            weather = {"temperature": 0.0, "humidity": 0.0}

        return {
            "nama": self.nama_kandidat,
            "data": {
                "sensor1": random.randint(0, 100),
                "sensor2": round(random.uniform(0, 1000), 2),
                "sensor3": random.choice([True, False]),
                "sensor4": weather.get("temperature"),
                "sensor5": weather.get("humidity")
            },
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }


    def writeCsvLog(self, data, status):
        """Logging data ke file CSV di direktori log [cite: 16, 246, 247, 250]"""
        if not os.path.exists("log"):
            os.makedirs("log")
            
        date_str = datetime.now().strftime("%d%m%y")
        file_name = f"log/mqtt_log_{date_str}.csv"
        
        file_exists = os.path.isfile(file_name)
        with open(file_name, mode="a", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            if not file_exists:
                writer.writerow(["timestamp", "sensor1", "sensor2", "sensor3", "sensor4", "sensor5", "status"])
            
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data["data"]["sensor1"],
                data["data"]["sensor2"],
                data["data"]["sensor3"],
                data["data"]["sensor4"],
                data["data"]["sensor5"],
                status
            ])