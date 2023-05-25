from queue import Queue
from time import sleep
from json import loads, dumps
from com.com_mqtt import MqttController 
from parking_controller.controller import ParkingController

input = Queue()
output = Queue()

controller = ParkingController(
    input_queue=input,
    output_queue=output,
)

communication_controller = MqttController(input, "broker.hivemq.com", 1883)

while True:
    communication_controller.loop()
    controller.loop()

    if not output.empty():
        communication_controller.publish(
            topic="EAFIT/PARKING_TEST/OUTPUT", 
            payload=dumps(output.get())
        )

    sleep(1)
