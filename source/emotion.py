import cv2
import matplotlib as plt
from deepface import DeepFace

cap = cv2.VideoCapture(0)
i = 1
emotion = " "
while True:
	_,img = cap.read()
	if(i>100):
		predictions = DeepFace.analyze(img)
		emotion = predictions['dominant_emotion']
		gender = predictions['gender']
	cv2.imshow(emotion,img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	i += 1

cv2.destroyAllWindows()
cap.release()
