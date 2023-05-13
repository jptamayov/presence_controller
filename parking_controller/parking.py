from dataclasses import dataclass

@dataclass
class Parking:
    id: str
    capacity: int
    occupancy: int = 0

    def get_input_topic(self) -> str:
        return f"EAFIT_PARKING/{self.id}/OUTPUT"
    
    def get_output_topic(self) -> str:
        return f"EAFIT_PARKING/{self.id}/INPUT"

    def update_occupancy(self, value: int) -> int:
        new_occupancy = self.occupancy + value
        if new_occupancy <= self.capacity and new_occupancy >= 0:
            self.occupancy = new_occupancy
            return self.occupancy
        else:
            raise ValueError(f"Invalid Value out of range: {new_occupancy}")

    @property
    def occupancy_percentage(self) -> float:
        return float(self.occupancy) / float(self.capacity)

    @property
    def dict(self) -> dict:
        return {
            "id": self.id,
            "capacity": self.capacity,
            "occupancy": self.occupancy,
            "occupancy_percentage": self.occupancy_percentage,
        }
