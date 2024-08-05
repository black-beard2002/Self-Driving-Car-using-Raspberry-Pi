import RPi.GPIO as GPIO
from time import sleep
from ultra import Sensor
import numpy as np
from PlateDetection.plate_detection import plateDetection
import WebcamModule as wM
import cv2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class motor():
    def __init__(self,Ena,In1,In2,In3,In4,Enb):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        self.Enb = Enb
        self.In3 = In3
        self.In4 = In4
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(self.Ena,GPIO.OUT)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)
        GPIO.setup(self.Enb,GPIO.OUT)
        GPIO.setup(self.In3,GPIO.OUT)
        GPIO.setup(self.In4,GPIO.OUT)
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In4,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.HIGH)
        self.pwma = GPIO.PWM(self.Ena, 100)
        self.pwma.start(0)
        self.pwmb = GPIO.PWM(self.Enb, 100)
        self.pwmb.start(0)
        self.pwma.ChangeDutyCycle(0)
        self.pwmb.ChangeDutyCycle(0)

    def follow(self, center_x, imgWidth):
        threshold = 0.15 * imgWidth  # Adjust threshold as needed
        if center_x < imgWidth/2 - threshold:
            # Plate is left of center, turn left
            GPIO.output(self.In1, GPIO.LOW)
            GPIO.output(self.In2, GPIO.HIGH)
            GPIO.output(self.In3, GPIO.LOW)
            GPIO.output(self.In4, GPIO.HIGH)
            self.pwma.ChangeDutyCycle(40)
            self.pwmb.ChangeDutyCycle(30)
        elif center_x > imgWidth/2 + threshold:
            # Plate is right of center, turn right
            GPIO.output(self.In1, GPIO.HIGH)
            GPIO.output(self.In2, GPIO.LOW)
            GPIO.output(self.In3, GPIO.HIGH)
            GPIO.output(self.In4, GPIO.LOW)
            self.pwma.ChangeDutyCycle(30)
            self.pwmb.ChangeDutyCycle(40)
        else:
            # Plate is centered, move forward
            GPIO.output(self.In1, GPIO.LOW)
            GPIO.output(self.In2, GPIO.HIGH)
            GPIO.output(self.In3, GPIO.HIGH)
            GPIO.output(self.In4, GPIO.LOW)
            self.pwma.ChangeDutyCycle(50)
            self.pwmb.ChangeDutyCycle(50)

    def stop(self,t=0):
        print("stop")
        self.pwma.ChangeDutyCycle(0)
        self.pwmb.ChangeDutyCycle(0)
        sleep(t)


def main():
    img,imgWidth = wM.getImg(display=False , size=[600, 400])
    img_orig = np.copy(img)
    img_with_plate, plate_coords, center_x = plateDetection.Detect(img_orig)
    distance = Sensor.get_distance()
    if distance>10:
        if len(plate_coords) > 0:
            cv2.imshow('Detected plate', img_with_plate)
            motor1.follow(center_x,imgWidth)
        else:
            motor1.stop()
        cv2.waitKey(1)
    else:
        print("stop!!!")
        motor1.stop()

if __name__ == '__main__':
    motor1 = motor(7,1,12,16,20,21)
    while True:
        main()