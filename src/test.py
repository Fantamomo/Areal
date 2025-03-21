import time
from src.Drone import Drone

if __name__ == '__main__' and False:
    drone = Drone()
    drone.connect()
    drone.take_off()
    time.sleep(2)

    # Drehung zu Beginn
    # drone.rotate(360)

    size = 0.5
    velocity = Drone.VELOCITY * 2
    base_height = drone.default_height
    start_position = (0, 0, base_height)

    # Effizienteste Route für den Würfel
    path = [
        start_position, (size, 0, base_height), (size, size, base_height), (0, size, base_height), start_position,
        (0, 0, base_height + size), (size, 0, base_height + size), (size, size, base_height + size),
        (0, size, base_height + size), (0, 0, base_height + size),
        (0, size, base_height + size), (0, size, base_height), (size, size, base_height),
        (size, size, base_height + size), (size, 0, base_height + size), (size, 0, base_height),
        start_position
    ]

    for wp in path:
        drone.move_to(*wp, mode="indirect", velocity=velocity)
        time.sleep(2)

    # Drehung am Ende
    # drone.rotate(360)

    drone.land()
    drone.disconnect()

# if __name__ == '__main__':
#     drone = Drone()
#     drone.connect()
#     drone.take_off()
#     time.sleep(2)
#
#     drone.move_to(0, 0, 1, mode = "indirect")
#     drone.move_to(1, 0, 2, mode = "indirect")
#     drone.move_to(0, 0, 1, mode = "indirect")
#
#     drone.land()