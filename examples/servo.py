import argparse
import time

from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

def linear_move(servo_id, start, end, speed=60, update_rate=50):
    # Calculate the number of seconds to wait between target updates to allow
    # the motor to move.
    # Units:  seconds = 1.0 / (cycles/second)
    interval = 1.0 / update_rate

    # Compute the size of each step in degrees.
    # Units:  degrees = (degrees/second) * second
    step = speed * interval

    # Output the start angle once before beginning the loop.  This guarantees at
    # least one angle will be output even if the start and end are equal.
    angle = start
    kit.servo[servo_id].angle = angle

    # Loop once for each incremental angle change.
    while angle != end:
        time.sleep(interval)            # pause for the sampling interval

        # Update the target angle.  The positive and negative movement directions
        # are treated separately.
        if end >= start:
            angle += step;              # movement in the positive direction
            if angle > end:
                angle = end             # end at an exact position
        else:
            angle -= step               # movement in the negative direction
            if angle < end:
                angle = end             # end at an exact position

        kit.servo[servo_id].angle = angle  # update the hardware

parser = argparse.ArgumentParser()

parser.add_argument('start', type=int, help='Start angle')
parser.add_argument('end', type=int, help='End angle')
parser.add_argument('speed', type=int, default=120,  help='Movement speed')
parser.add_argument('-s', '--servo', type=int, default=2, help='Servo id')

args = parser.parse_args()

linear_move (args.servo, args.start, args.end, args.speed)
