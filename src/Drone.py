import math
import sys
import atexit
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
        self.position: list[float] = [0.0, 0.0, default_height]  # x, y, z
        self.scf = None
        self.mc = None
        self.allow_experimental = False
        self.__is_land_on_programm_exit__ = False
        self.angle = 0.0
        cflib.crtp.init_drivers(enable_debug_driver=False)

    def land_on_programm_exit(self):
        if not self.__is_land_on_programm_exit__:
            atexit.register(self.land)
            self.__is_land_on_programm_exit__ = True

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
        """
        :param x: Moves the drone forward
        :param y: Moves the drone to the sites
        :param z: height
        :param velocity:
        :param mode: 'direct': The drone moves direct to the point, that could lead to that the drone moves diagonal.
        'indirect': The drone moves indirectly, that means, it will only moves at the x, y, z coordinate one at a time.
        :return:
        """
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

            self.angle += angle
            self.angle %= 360

    def circle(self, radius: float, velocity: float = VELOCITY):
        if self.mc:
            self.logger.info(f"Flying in a circle with radius {radius}")
            self.mc.circle_right(radius, velocity)

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

    def tuple_position(self):
        return tuple(self.position)

    def zigzag(self, length: float, width: float, steps: int, velocity: float = VELOCITY):
        if self.mc and self.allow_experimental:
            self.logger.info(f"Flying in zigzag pattern with length {length}, width {width} and {steps} steps")
            step_length = length / steps
            direction = 1
            for _ in range(steps):
                self.mc.move_distance(step_length, direction * width, 0, velocity)
                direction *= -1

    def spiral_up(self, height: float, radius: float, turns: int = 3, duration: float = 5.0,
                  velocity: float = VELOCITY):
        if self.mc and self.allow_experimental:
            self.logger.info(f"Ascending in a spiral: height={height}, radius={radius}, turns={turns}")
            step_height = height / turns
            for _ in range(turns):
                self.mc.circle_right(radius, duration / turns)
                self.mc.move_distance(0, 0, step_height, velocity)

    def wave_flight(self, length: float, amplitude: float, waves: int, velocity: float = VELOCITY):
        if self.mc and self.allow_experimental:
            self.logger.info(f"Flying in a wave pattern with length {length}, amplitude {amplitude}, waves {waves}")
            step_length = length / (waves * 10)
            for i in range(waves * 10):
                y_offset = amplitude * math.sin((i / (waves * 10)) * 2 * math.pi)
                self.mc.move_distance(step_length, y_offset, 0, velocity)

    def adjust_height(self, target_height: float, velocity: float = VELOCITY):
        if self.mc:
            dz = target_height - self.position[2]
            self.logger.info(f"Adjusting height to {target_height}")
            self.mc.move_distance(0, 0, dz, velocity)
            self.position[2] = target_height

    def follow_path(self, waypoints: list[tuple[float, float, float]], velocity: float = VELOCITY):
        if self.mc:
            self.logger.info(f"Following path with {len(waypoints)} waypoints")
            for x, y, z in waypoints:
                self.move_to(x, y, z, velocity)

    def return_to_start(self, velocity: float = VELOCITY, mode: str = "direct"):
        if self.mc:
            self.logger.info("Returning to start position considering rotation")

            # Berechnung der relativen Distanz zum Startpunkt
            dx = -self.position[0]
            dy = -self.position[1]

            # Umrechnung in globale Koordinaten basierend auf der Rotation
            angle_rad = math.radians(self.angle)
            global_dx = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            global_dy = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)

            # Bewegung zurück zum Startpunkt
            self.move_to(global_dx, global_dy, self.default_height, velocity, mode)
