import RPi.GPIO as GPIO
import time
import signal
import sys
import send_email
from creds import TO

def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    GPIO.cleanup()
    sys.exit(0)


def calculate_distance_mean():
    # use Raspberry Pi board pin numbers
    GPIO.setmode(GPIO.BCM)

    # set GPIO Pins
    pinTrigger = 18
    pinEcho = 24

    signal.signal(signal.SIGINT, close)

    # set GPIO input and output channels
    GPIO.setup(pinTrigger, GPIO.OUT)
    GPIO.setup(pinEcho, GPIO.IN)

    readings = 20
    i = 0
    distance = 0.0
    cumulative_distance = 0.0

    while i < readings:
        # set Trigger to HIGH
        GPIO.output(pinTrigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(pinTrigger, False)

        startTime = time.time()
        stopTime = time.time()

        # save start time
        while 0 == GPIO.input(pinEcho):
            startTime = time.time()

        # save time of arrival
        while 1 == GPIO.input(pinEcho):
            stopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = stopTime - startTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        print("Distance: %.1f cm" % distance)
        time.sleep(1)
        i += 1
        cumulative_distance += distance

    dist_average = round((cumulative_distance / readings), 2)

    print("Average distance: {}".format(dist_average))
    return dist_average


def level_notifier(distance):
    if distance > 14:
        return "getting low"
    else:
        return "okay"


salt_level = calculate_distance_mean()

if salt_level > 13.5:
    msg = """\
    Subject: Salt Level

    This message is sent from your water softener.
    Yeah, that's right, your water softener is now
    self-aware.

    The salt is {0} cm from the sensor. Might wanna
    add a bag or two.
    """.format(salt_level)
    for recipient in TO:
        send_email.send_mail(msg=msg, to=recipient)
