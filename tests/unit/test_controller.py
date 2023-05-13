import pytest

from queue import Queue
from parking_controller.parking import Parking
from parking_controller.controller import ParkingController
from parking_controller.repository import DummyRepository



def test_controller():
    input_queue = Queue()
    output_queue = Queue()

    test_controller = ParkingController(
        input_queue=input_queue,
        output_queue=output_queue,
        repository=DummyRepository(),
    )
    
    assert test_controller.parkings == {}

    test_controller.register(data={
        "id": "EafitIng",
        "capacity": 200
    })

    assert len(test_controller.parkings) == 1
    assert output_queue.get() == {"register": 1}

    test_controller.update(id="EafitIng", value=1)

    assert test_controller.parkings["EafitIng"].occupancy == 1
    
    input_queue.put({
        "topic": "REGISTRO", 
        "payload": {"id": "EafitIdiomas", "capacity":50}
    })

    test_controller.loop()
    
    assert len(test_controller.parkings) == 2

    input_queue.put({
        "topic": "OPERACION", 
        "payload": {"id": "EafitIdiomas", "value": 1}
    })

    test_controller.loop()

    assert test_controller.parkings["EafitIdiomas"].occupancy == 1
    assert test_controller.parkings["EafitIdiomas"].occupancy_percentage == float(1) / float(50)

    assert output_queue.get({"id": "EafitIdiomas", "ocupancy": float(1) / 50})