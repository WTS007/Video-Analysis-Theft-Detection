import cv2
import time
import datetime

cap = cv2.VideoCapture(0)
_, frame = cap.read()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 10

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

flag = False
#ix = -1
#iy = -1
z = 0
cord = []


def crop(event,x,y,flags,params):
	global z
	global cord
	global frame
	ix,iy=0,0
	if event == 1:
		ix = x
		iy = y
		flag = True
	elif event == 4:
		fx = x
		fy = y
		flag = False
		cv2.rectangle(frame,pt1=(ix,iy),pt2=(x,y),thickness = 1,color=(0,0,0))
		cord = [iy,fy,ix,fx]
		frame = frame[iy:fy,ix:fx]
		#cv2.imshow('', frame)
		#cv2.waitKey(0)
		cord = [iy,fy,ix,fx]
	z = 1









cv2.namedWindow(winname = "Select_Restricted_Area")
cv2.setMouseCallback("Select_Restricted_Area",crop)

while True:
	_, frame = cap.read()
	cv2.imshow("Select_Restricted_Area",frame)
	if cv2.waitKey(1) & 0xFF == ord('x'):
		break
		
		
		
while True:
	_, frame = cap.read()
	p,q,r,s = cord[0],cord[1],cord[2],cord[3]
	frame = frame[p:q,r:s]
	frame = cv2.resize(frame,(0,0),fx=2,fy=2)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, width, height) in faces:
		    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)
	if (z == 1):
		if len(faces) + len(bodies) > 0:
			if detection:
			    timer_started = False
			else:
			    detection = True
			    current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
			    out = cv2.VideoWriter(
			        f"{current_time}.mp4", fourcc, 25, frame_size)
			    print("Started Recording!")
		elif detection:
			if timer_started:
			    if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
			        detection = False
			        timer_started = False
			        out.release()
			        print('Stop Recording!')
			else:
			    timer_started = True
			    detection_stopped_time = time.time()

		if detection:
			out.write(frame)


		cv2.imshow("Camera", frame)

		if cv2.waitKey(1) == ord('q'):
			break

out.release()
cap.release()
cv2.destroyAllWindows()
