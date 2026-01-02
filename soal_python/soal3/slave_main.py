import time
from pyModbusTCP.server import ModbusServer
from function.modbus_helper import ModbusHelper


class MyModbusSlave:
    def __init__(self):
        self.server = ModbusServer(host="0.0.0.0", port=5020, no_block=True)
        self.helper = ModbusHelper()


    def updateRegisters(self):
        """Setiap 5 detik, update nilai suhu dan kelembaban ke register"""
        data = self.helper.readWeatherData()
        
        self.server.data_bank.set_holding_registers(0, [int(data["temperature"] * 100)])
        self.server.data_bank.set_holding_registers(1, [int(data["humidity"] * 100)])
        
        status = self.server.data_bank.get_holding_registers(2)[0]
        state_text = "RUNNING" if status == 1 else "STOPPED"
        print(f"Slave Data Updated | Status: {state_text}")


    def run(self):
        print("Starting Modbus Slave on port 5020...")
        self.server.start()
        try:
            while True:
                self.updateRegisters()
                time.sleep(5)
        except KeyboardInterrupt:
            self.server.stop()


if __name__ == "__main__":
    slave = MyModbusSlave()
    slave.run()