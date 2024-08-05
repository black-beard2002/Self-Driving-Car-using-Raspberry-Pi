import cv2
import numpy as np
from tensorflow.keras.models import load_model
from SignDetection.stop_sign_detection import signDetection
from ultra import Sensor
import WebcamModule as wM
import MotorModule as mM
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#######################################
buzzer_pin = 26
GPIO.setup(buzzer_pin, GPIO.OUT)
steeringSen = 0.78 # Steering Sensitivity
maxThrottle = 0.16  # Forward Speed %
motor = mM.Motor(7, 1, 12, 16, 20, 21)  # Pin Numbers
model = load_model('/home/pi/Desktop/project/modelGRAY3.h5')
#######################################
GPIO.setup(17, GPIO.OUT)
GPIO.setup(0, GPIO.OUT)
def preProcess(img):
    img = img[55:120,50:230, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    img = np.expand_dims(img, axis=-1)  # Add this line to create a single channel
    img = np.repeat(img, 3, axis=-1)  # Repeat the single channel to create 3 channels
    return img

def stopAndContinue(stop_img):
    cv2.imshow("Stop Sign", stop_img)
    cv2.waitKey(1)
    sleep(1)
    motor.stop()

def stopAndReturn(n, stop_img):
    print("Signs detected: ", n)
    cv2.imshow("Stop Sign", stop_img)
    cv2.waitKey(1)
    motor.stop()
    sleep(3)
    motor.fullRotate()
    sleep(1)
    motor.stop()
    motor.move(maxThrottle, steering*steeringSen)

while True:
    img = wM.getImg(True, size=[240, 120])
    img_orig = img.copy()
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    """try:
        distance = Sensor.get_distance()
    except UnboundLocalError:
        pass
    if 7.5<distance<11:
        GPIO.output(buzzer_pin, GPIO.HIGH)
        motor.stop(1)
        motor.avoid()
        GPIO.output(buzzer_pin, GPIO.LOW)
        motor.stop(1)
    steering = float(model.predict(img))
    print(steering)
    stop_img, signs = signDetection.Detect(img_orig)
    numberOfSigns = len(signs)
    if numberOfSigns == 0:
        try:
            GPIO.output(17, GPIO.LOW)
            GPIO.output(0, GPIO.LOW)
            cv2.destroyWindow("Stop Sign")
        except:
            pass
        motor.move(maxThrottle, steering * steeringSen)
    elif numberOfSigns == 1:
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(0, GPIO.HIGH)
        stopAndContinue(stop_img)
    elif numberOfSigns==3:
        motor.move(maxThrottle, steering * steeringSen)
        sleep(3)
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(0, GPIO.HIGH)
        stopAndReturn(numberOfSigns, stop_img)"""
    steering = float(model.predict(img))
    motor.move(maxThrottle, steering * steeringSen)
    cv2.waitKey(1)