from queue import Queue
from parking_controller.parking import Parking

class ParkingController:
    def __init__(self, input_queue: Queue, output_queue: Queue) -> None:
        self.__parkings = {}
        self.__input_queue = input_queue
        self.__output_queue = output_queue
    
    @property
    def parkings(self) -> dict[str, Parking]:
        return self.__parkings

    def register(self, data: dict) -> Parking:
        parking = Parking(
            id=data["id"],
            capacity=data["capacity"],
        )
        self.__parkings[parking.id] = parking
        self.__output_queue.put({"register": 1})
        return parking
    
    def update(self, id: str, value: int):
        parking = self.parkings[id]
        parking.update_occupancy(value=value)

    def loop(self):
        if not self.__input_queue.empty():
            message = self.__input_queue.get()
            topic = message["topic"]
            payload = message["payload"]

            if topic == "REGISTRO":
                self.register(data=payload)
            
            elif topic == "OPERACION":
                self.update(id=payload["id"], value=payload["value"])
                self.__output_queue.put({
                    "id": payload["id"],
                    "ocuppancy": self.parkings[payload["id"]].occupancy_percentage
                })
    