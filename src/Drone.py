import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander


class Drone:
    VELOCITY = 0.2
    RATE = 360.0 / 5

    def __init__(self, uri: str = 'radio://0/80/2M', default_height: float = 0.3):
        self.mc: MotionCommander | None = None
        self.scf: SyncCrazyflie | None = None
        self.uri: str = uri
        cflib.crtp.init_drivers(enable_debug_driver=False)

        self.default_height = default_height

    def connect(self):
        self.scf = SyncCrazyflie(self.uri)
        self.scf.open_link()
        self.scf.cf.platform.send_arming_request(True)
        time.sleep(1.0)
        self.mc = MotionCommander(self.scf, self.default_height)

    def take_off(self):
        self.mc.take_off()

    def land(self):
        self.mc.land()

    def forward(self, distance_m: float, velocity: float = VELOCITY):
        self.mc.forward(distance_m, velocity)
