import json
import struct


class ModbusHelper:
    @staticmethod
    def readWeatherData():
        """Membaca data suhu dan kelembaban dari file JSON soal no 2"""
        try:
            with open("log/data_weather.json", "r") as f:
                return json.load(f)
        except Exception:
            # Data dummy jika file belum ada
            return {"temperature": 0.0, "humidity": 0.0}


    @staticmethod
    def floatToRegisters(value):
        """Mengonversi float ke dalam 2 buah holding registers (32-bit total)"""
        packed = struct.pack(">f", round(value, 2))
        return struct.unpack(">HH", packed)


    @staticmethod
    def registersToFloat(registers):
        """Mengonversi 2 buah holding registers kembali ke float"""
        packed = struct.pack(">HH", *registers)
        return round(struct.unpack(">f", packed)[0], 2)