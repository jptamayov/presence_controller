from paho.mqtt import client as mqtt
from queue import Queue
from json import loads, dumps

#class Mqtt_Controller(mqtt.Client):
class Mqtt_Controller():

    def __init__(self, input_queue: Queue) -> None:
        self.__input_queue = input_queue

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("EAFIT/PARKING_TEST/INPUT")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        payload = loads(msg.payload)
        self.__input_queue.put(payload)

    def setup(self):
        client = mqtt.Client()
        client.on_message = self.on_message
        client.on_connect = self.on_connect
        client.connect("broker.hivemq.com", 1883, 60)
        return client
