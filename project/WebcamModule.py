import cv2
from picamera2 import Picamera2
from SignDetection.stop_sign_detection import signDetection
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1920,1080)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

def getImg(display= True,size=[240,120]):
    img= picam2.capture_array()
    img = cv2.resize(img,(size[0],size[1]))
    if display:
        cv2.imshow('IMG',img)
        cv2.waitKey(1)
        """img = img[55:120,50:230, :]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.resize(img, (200, 66))
        img = img / 255
        cv2.imshow('IMG2',img)
        cv2.waitKey(1)"""
    return img

if __name__ == '__main__':
    while True:
        img = getImg(True)