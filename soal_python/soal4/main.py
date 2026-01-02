import time
import json
import sys
import os
import paho.mqtt.client as mqtt
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from function.mqtt_helper import MqttHelper


class MqttClientNode:
    def __init__(self, nama):
        self.NAMA = nama
        self.TOPIC_DATA = f"mqtt/{self.NAMA}/data"
        self.TOPIC_CMD = f"mqtt/{self.NAMA}/command"
        self.BROKER = "test.mosquitto.org"
        
        self.helper = MqttHelper(self.NAMA)
        self.client = mqtt.Client()
        self.is_active = True
        self.interval = 5


    def onConnect(self, client, userdata, flags, rc):
        """Callback saat terhubung ke broker [cite: 261]"""
        print(f"Connected to Broker with result code {rc}")
        self.client.subscribe(self.TOPIC_CMD)


    def onMessage(self, client, userdata, msg):
        """Callback saat menerima pesan subscribe [cite: 261, 263, 283]"""
        try:
            payload = json.loads(msg.payload.decode())
            cmd = payload.get("command", "")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\nTimestamp: {timestamp}\nAction: Subscribe\nTopic: {msg.topic}\nData: {payload}")

            if cmd == "pause":
                self.is_active = False
            elif cmd == "resume":
                self.is_active = True
            elif "set_interval" in cmd:
                new_interval = int(cmd.split(":")[1])
                self.interval = new_interval
        except Exception as e:
            print(f"Error command: {e}")


    def run(self):
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.BROKER, 1883, 60)
        self.client.loop_start()

        try:
            while True:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                if self.is_active:
                    data_pack = self.helper.getSensorData()
                    result = self.client.publish(self.TOPIC_DATA, json.dumps(data_pack))
                    
                    status = "Success" if result.rc == mqtt.MQTT_ERR_SUCCESS else "Failed"
                    self.helper.writeCsvLog(data_pack, status)
                    print(f"\nTimestamp: {timestamp}\nAction: Publish\nTopic: {self.TOPIC_DATA}\nData: {data_pack}\nState: {status}")
                else:
                    print(f"\nTimestamp: {timestamp}\nAction: Publish\nState: Inactive")

                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.client.loop_stop()
            self.client.disconnect()


if __name__ == "__main__":
    node = MqttClientNode(nama="syaihan") 
    node.run()