from paho.mqtt import client as mqtt
from queue import Queue
from json import loads, dumps

class MqttController(mqtt.Client):

    def __init__(self, input_queue: Queue, broker, port) -> None:
        mqtt.Client.__init__(self)
        self.__input_queue = input_queue
        self.__broker = broker
        self.__port = port
        self.connect(self.__broker, self.__port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.subscribe("EAFIT/PARKING_TEST/INPUT")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        payload = loads(msg.payload)
        self.__input_queue.put(payload)
