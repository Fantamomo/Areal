import logging

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander


class Drone:
    VELOCITY = 0.2
    logger: logging.Logger
    uri: str
    default_height: float
    position: list[float]
    scf: SyncCrazyflie | None
    mc: MotionCommander | None
    __is_land_on_programm_exit__: bool
    allow_experimental: bool
    angle: float

    def __init__(self, uri: str = 'radio://0/80/2M', default_height: float = 0.3):
        ...

    def land_on_programm_exit(self):
        ...

    def connect(self):
        ...

    def take_off(self):
        ...

    def land(self):
        ...

    def move_to(self, x: float, y: float, z: float = None, velocity: float = VELOCITY, mode: str = "direct"):
        ...

    def rotate(self, angle: float):
        ...

    def circle(self, radius: float, duration: float = 5.0):
        ...

    def emergency_stop(self):
        ...

    def get_position(self):
        ...

    def disconnect(self):
        ...

    def tuple_position(self):
        ...

    # Experimental
    def zigzag(self, length: float, width: float, steps: int, velocity: float = VELOCITY):
        ...

    # Experimental
    def spiral_up(self, height: float, radius: float, turns: int = 3, duration: float = 5.0):
        ...

    # Experimental
    def wave_flight(self, length: float, amplitude: float, waves: int, velocity: float = VELOCITY):
        ...

    # Experimental
    def adjust_height(self, target_height: float, velocity: float = VELOCITY):
        ...

    # Experimental
    def follow_path(self, waypoints: list[tuple[float, float, float]], velocity: float = VELOCITY):
        ...

    def return_to_start(self, velocity: float = VELOCITY, mode: str = "direct"):
        ...