import sys
import time
import logging

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander


class Drone:
    VELOCITY = 0.2

    def __init__(self, uri: str = 'radio://0/80/2M', default_height: float = 0.3):
        self.logger = logging.getLogger("drone")
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("Initializing Drone")

        self.uri = uri
        self.default_height = default_height
        self.position = [0.0, 0.0, default_height]  # x, y, z
        self.scf = None
        self.mc = None
        cflib.crtp.init_drivers(enable_debug_driver=False)

    def connect(self):
        self.logger.info("Connecting to Drone")
        try:
            self.scf = SyncCrazyflie(self.uri)
            self.scf.open_link()
            self.scf.cf.param.set_value("commander.enHighLevel", "1")
            self.mc = MotionCommander(self.scf, self.default_height)
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")

    def take_off(self):
        if self.mc:
            self.logger.info("Taking off!")
            self.mc.take_off()
            self.position[2] = self.default_height

    def land(self):
        if self.mc:
            self.logger.info("Landing!")
            self.mc.land()
            self.position[2] = 0.0

    def move_to(self, x: float, y: float, z: float = None, velocity: float = VELOCITY, mode: str = "direct"):
        if self.mc:
            target_z = self.position[2] if z is None else z
            self.logger.info(f"Moving to: ({x}, {y}, {target_z}) with mode: {mode}")

            if mode == "direct":
                dx, dy, dz = x - self.position[0], y - self.position[1], target_z - self.position[2]
                self.mc.move_distance(dx, dy, dz, velocity)
            elif mode == "indirect":
                dz = target_z - self.position[2]
                if dz != 0:
                    self.mc.move_distance(0, 0, dz, velocity)
                dx = x - self.position[0]
                if dx != 0:
                    self.mc.move_distance(dx, 0, 0, velocity)
                dy = y - self.position[1]
                if dy != 0:
                    self.mc.move_distance(0, dy, 0, velocity)
            else:
                self.logger.error("Invalid mode! Use 'direct' or 'indirect'")
                return

            self.position = [x, y, target_z]

    def rotate(self, angle: float):
        if self.mc:
            self.logger.info(f"Rotating {angle} degrees")
            self.mc.turn_left(angle) if angle > 0 else self.mc.turn_right(-angle)

    def circle(self, radius: float, duration: float = 5.0):
        if self.mc:
            self.logger.info(f"Flying in a circle with radius {radius}")
            self.mc.circle_right(radius, duration)

    def emergency_stop(self):
        if self.scf:
            self.logger.warning("Emergency stop activated!")
            self.scf.cf.high_level_commander.stop()

    def get_position(self):
        return tuple(self.position)

    def disconnect(self):
        if self.scf:
            self.logger.info("Disconnecting from Drone")
            self.scf.close_link()
            self.scf = None
            self.mc = None