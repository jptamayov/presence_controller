from queue import Queue
from time import sleep
from json import loads, dumps
import paho.mqtt.client as mqtt
from parking_controller.controller import ParkingController


input = Queue()
output = Queue()

controller = ParkingController(
    input_queue=input,
    output_queue=output,
)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("EAFIT/PARKING_TEST/INPUT")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    payload = loads(msg.payload)
    input.put(payload)


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect("broker.hivemq.com", 1883, 60)

while True:
    client.loop()
    controller.loop()

    if not output.empty():
        client.publish(
            topic="EAFIT/PARKING_TEST/OUTPUT", 
            payload=dumps(output.get())
        )

    sleep(1)
