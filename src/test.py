
import time
from src.Drone import Drone
import tasks

drone: Drone = None

def init():
    global drone
    drone = Drone()
    drone.allow_experimental = True
    drone.land_on_programm_exit()

    drone.connect()

def end():
    drone.land()
    drone.disconnect()

if __name__ == '__main__':
    init()

    drone.take_off()
    time.sleep(2)

    base_height = drone.position[2]

    tasks.cube_size = 0.7
    tasks.cube(drone)

    # drone.move_to(0, 0, 1)


    end()