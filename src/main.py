
if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI) as scf:
        # Arm the Crazyflie
        scf.cf.platform.send_arming_request(True)
        time.sleep(1.0)

        # We take off when the commander is created
        with MotionCommander(scf) as mc:
            print('Taking off!')
            time.sleep(1)

            # There is a set of functions that move a specific distance
            # We can move in all directions
            print('Moving forward 0.5m')
            mc.forward(0.25)
            # Wait a bit
            time.sleep(1)

            print('Moving up 0.2m')
            mc.up(0.1)
            # Wait a bit
            time.sleep(1)

            print('Doing a 270deg circle');
            mc.circle_right(0.5, velocity=0.5, angle_degrees=270)

            print('Moving down 0.2m')
            mc.down(0.1)
            # Wait a bit
            time.sleep(1)

            print('Rolling left 0.2m at 0.6m/s')
            mc.left(0.2, velocity=0.6)
            # Wait a bit
            time.sleep(1)

            print('Moving forward 0.5m')
            mc.forward(0.25)

            # We land when the MotionCommander goes out of scope
            print('Landing!')