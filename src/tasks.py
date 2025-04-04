import time

from src.Drone import Drone

cube_size = 0.5


def cube(drone: Drone, velocity: float = Drone.VELOCITY * 2.5):
    path = [
        (0, 0, 0),
        (cube_size, 0, 0),
        (cube_size, cube_size, 0),
        (0, cube_size, 0),
        (0, 0, 0),

        (0, 0, cube_size),
        (cube_size, 0, cube_size),
        (cube_size, cube_size, cube_size),
        (0, cube_size, cube_size),

        (0, 0, cube_size),
        (0, cube_size, cube_size),
        (0, cube_size, 0),
        (cube_size, cube_size, 0),
        (cube_size, cube_size, cube_size),
        (cube_size, 0, cube_size),
        (cube_size, 0, 0),

        (0, 0, 0)
    ]
    start_position = drone.tuple_position()

    absolute_path = [(start_position[0] + x, start_position[1] + y, start_position[2] + z) for x, y, z in path]

    for wp in absolute_path:
        drone.move_to(*wp, mode="indirect", velocity=velocity)
        time.sleep(0.87) # 1.25
