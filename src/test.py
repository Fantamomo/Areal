import time

from src.Drone import Drone

if __name__ == '__main__':
    drone = Drone()
    drone.connect()
    drone.take_off()
    time.sleep(1)
    drone.land()