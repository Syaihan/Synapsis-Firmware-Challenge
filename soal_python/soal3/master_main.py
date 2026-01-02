import time
from datetime import datetime
from pyModbusTCP.client import ModbusClient


class MyModbusMaster:
    def __init__(self):
        self.client = ModbusClient(host="localhost", port=5020, auto_open=True)
        self.toggle_status = 1


    def readAndControl(self):
        start_time = time.time()
        last_control_time = 0

        try:
            while True:
                current_time = time.time()
                
                # Setiap 5 detik baca register 0, 1, 2
                regs = self.client.read_holding_registers(0, 3)
                if regs:
                    suhu = regs[0] / 100.0
                    hum = regs[1] / 100.0
                    status = "RUNNING" if regs[2] == 1 else "STOPPED"
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"({timestamp} GMT+7) | Suhu: {suhu}°C | Hum: {hum}% | Status: {status}")

                # Setiap 30 detik melakukan control/write ke register 2 (0/1 bergantian)
                if current_time - last_control_time >= 30:
                    self.client.write_single_register(2, self.toggle_status)
                    print(f"---> Master: Change Status to {self.toggle_status}")
                    self.toggle_status = 0 if self.toggle_status == 1 else 1
                    last_control_time = current_time

                time.sleep(5)
        except KeyboardInterrupt:
            self.client.close()


if __name__ == "__main__":
    master = MyModbusMaster()
    master.readAndControl()