from queue import Queue
from time import sleep
from json import loads, dumps
from com.com_mqtt import Mqtt_Controller as mqtt_controller
from parking_controller.controller import ParkingController

input = Queue()
output = Queue()

controller = ParkingController(
    input_queue=input,
    output_queue=output,
)

communication_controller = mqtt_controller(input)
client = communication_controller.setup()

while True:
    client.loop()
    controller.loop()

    if not output.empty():
        client.publish(
            topic="EAFIT/PARKING_TEST/OUTPUT", 
            payload=dumps(output.get())
        )

    sleep(1)
