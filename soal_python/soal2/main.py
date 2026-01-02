import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function.weather_helper import WeatherService


class WeatherScheduler:
    def __init__(self):
        self.weather_service = WeatherService()


    def start(self):
        print("--- Weather Sampling Scheduler ---")
        
        while True:
            user_input = input("Masukkan interval sampling (detik): ")
            
            if user_input.isdigit() and int(user_input) > 0:
                interval = int(user_input)
                break
            else:
                print("Input tidak valid! Harap masukkan angka di atas 0")

        print(f"Scheduler dimulai dengan interval {interval} detik...")
        
        try:
            while True:
                self.weather_service.getWeatherData()
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nProgram dihentikan.")


if __name__ == "__main__":
    scheduler = WeatherScheduler()
    scheduler.start()