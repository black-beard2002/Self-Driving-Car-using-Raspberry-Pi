import lgpio as GPIO
import time

# Set pins
TRIG = 14  # Associate pin 23 to TRIG
ECHO = 15  # Associate pin 24 to ECHO

# Open the GPIO chip and set the GPIO direction
h = GPIO.gpiochip_open(0)
GPIO.gpio_claim_output(h, TRIG)
GPIO.gpio_claim_input(h, ECHO)

class Sensor:
    def get_distance():
        # Set TRIG LOW
        GPIO.gpio_write(h, TRIG, 0)
        time.sleep(0.20)
        # Send 10us pulse to TRIG
        GPIO.gpio_write(h, TRIG, 1)
        time.sleep(0.00001)
        GPIO.gpio_write(h, TRIG, 0)

        # Start recording the time when the wave is sent
        while GPIO.gpio_read(h, ECHO) == 0:
            pulse_start = time.time()

        # Record time of arrival
        while GPIO.gpio_read(h, ECHO) == 1:
            pulse_end = time.time()

        # Calculate the difference in times
        try:
            pulse_duration = pulse_end - pulse_start
        except UnboundLocalError:
            print()

        # Multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        return distance
if __name__=='__main__':
    s = Sensor
    while True:
        try:
            d=s.get_distance()
            print("distance: ",d)
        except UnboundLocalError:
            continue