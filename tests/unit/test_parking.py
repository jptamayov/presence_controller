import pytest

from parking_controller.parking import Parking

def tests_parking():
    ID = "tests"
    CAPACITY = 10 

    dummy_parking  = Parking(
        id=ID,
        capacity=CAPACITY
    )

    assert dummy_parking.get_input_topic() == f"EAFIT_PARKING/{ID}/OUTPUT"
    assert dummy_parking.get_output_topic() == f"EAFIT_PARKING/{ID}/INPUT"

    with pytest.raises(ValueError):
        dummy_parking.update_occupancy(value=-1)
    
    with pytest.raises(ValueError):
        dummy_parking.update_occupancy(value= CAPACITY + 1)

    for i in range(CAPACITY):
        assert dummy_parking.update_occupancy(value= 1) == i + 1
    
    assert dummy_parking.occupancy_percentage == 1
    dummy_parking.update_occupancy(value= -CAPACITY)
    assert dummy_parking.occupancy_percentage == 0
    dummy_parking.update_occupancy(value=(CAPACITY / 2))
    assert dummy_parking.occupancy_percentage == 0.5
    
    assert dummy_parking.dict == {
        "id": ID,
        "capacity": CAPACITY,
        "occupancy": CAPACITY / 2,
        "occupancy_percentage": 0.5,
    }