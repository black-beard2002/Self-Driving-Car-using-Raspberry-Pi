import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from ultra import Sensor


class Motor():
    def __init__(self,EnA,In1,In2,In3,In4,EnB):
        self.EnA= EnA
        self.In1 = In1
        self.In2 = In2
        self.EnB= EnB
        self.In3 = In3
        self.In4 = In4
        GPIO.setup(self.EnA,GPIO.OUT);GPIO.setup(self.In1,GPIO.OUT);GPIO.setup(self.In2,GPIO.OUT)
        GPIO.setup(self.EnB,GPIO.OUT);GPIO.setup(self.In3,GPIO.OUT);GPIO.setup(self.In4,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnA, 100);
        self.pwmB = GPIO.PWM(self.EnB, 100);
        self.pwmA.start(0);
        self.pwmB.start(0);
        #Left_LED_PIN = 17
        #Right_LED_PIN = 0
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(0, GPIO.OUT)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(0, GPIO.LOW)
    def move(self,speed=0.5,turn=0,t=0):
        speed *=100
        turn *=70
        leftSpeed = speed-turn
        rightSpeed = speed+turn
        #reset settings to default before proceeding
        GPIO.output(self.In1,GPIO.LOW);GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.HIGH);GPIO.output(self.In4,GPIO.LOW)
        if leftSpeed>100: leftSpeed =100
        elif leftSpeed<-100: leftSpeed = -100
        if rightSpeed>100: rightSpeed =100
        elif rightSpeed<-100: rightSpeed = -100
        #print(leftSpeed,rightSpeed)
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        if leftSpeed>0:GPIO.output(self.In1,GPIO.LOW);GPIO.output(self.In2,GPIO.HIGH)
        else:GPIO.output(self.In1,GPIO.HIGH);GPIO.output(self.In2,GPIO.LOW)
        if rightSpeed>0:GPIO.output(self.In3,GPIO.HIGH);GPIO.output(self.In4,GPIO.LOW)
        else:GPIO.output(self.In3,GPIO.LOW);GPIO.output(self.In4,GPIO.HIGH)
        sleep(t)

    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);

    def fullRotate(self):
        self.pwmA.ChangeDutyCycle(100);
        self.pwmB.ChangeDutyCycle(100);
        GPIO.output(self.In1,GPIO.LOW);GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.LOW);GPIO.output(self.In4,GPIO.HIGH)
        sleep(0.52)

    def avoid(self):
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.LOW)
        GPIO.output(self.In4,GPIO.HIGH)
        self.pwmA.ChangeDutyCycle(70)
        self.pwmB.ChangeDutyCycle(70)
        sleep(0.23)
        GPIO.output(self.In3,GPIO.HIGH)
        GPIO.output(self.In4,GPIO.LOW)
        sleep(0.5)
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        sleep(0.4)
        GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In1,GPIO.LOW)
        sleep(0.43)
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.LOW)
        GPIO.output(self.In4,GPIO.HIGH)
        sleep(0.27)
if __name__=="__main__":
    motor = Motor(7, 1, 12, 16, 20, 21)
    motor.fullRotate()
    motor.stop()
    print("start")
    try:
        distance = Sensor.get_distance()
    except UnboundLocalError:
        pass
    if 7.5<distance<11:
        print(distance)
        motor.stop(1)
        motor.avoid()
        motor.stop()