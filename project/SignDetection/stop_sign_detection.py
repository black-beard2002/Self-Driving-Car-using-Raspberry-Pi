import cv2

class signDetection:
    @staticmethod
    def Detect(img):
        # Stop Sign Cascade Classifier xml
        stop_sign_cascade = cv2.CascadeClassifier('/home/pi/Desktop/project/SignDetection/cascade_stop_sign.xml')

        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect stop signs
        stop_signs = stop_sign_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)

        # Draw rectangles around detected stop signs
        for (x, y, w, h) in stop_signs:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(img, "Stop Sign", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

        return img, stop_signs