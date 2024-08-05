import cv2

class plateDetection:
    @staticmethod
    def Detect(img):
        # plate Cascade Classifier xml
        plate_cascade = cv2.CascadeClassifier('/home/pi/Desktop/project/PlateDetection/haarcascade_russian_plate_number.xml')
        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        center_x=0
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,minSize=(30,30))
        for (x, y, w, h) in plates:
            # Draw rectangle around the plate
            center_x = x+w//2
            center_y = y+h//2
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 3)
            # Draw a dot at the center of plate
            cv2.circle(img,(center_x,center_y),5,(0,0,255),-1)
            # plate text
            plate_text = f"plate:({center_x},{center_y})"
            # Write "plate" on the bottom of the rectangle
            cv2.putText(img, text="plate", org=(x, y-10),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 255, 0),thickness=2)

        return img, plates,center_x