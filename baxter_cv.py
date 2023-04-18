#from imutils.object_detection import non_max_suppression
#import pytesseract
#import argparse
import cv2
import numpy as np
import apriltag
from ultralytics import YOLO
from sklearn import cluster

'''
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

font_scale = 1.5
font = cv2.FONT_HERSHEY_PLAIN



cntr = 0;

while True:
	ret, frame = baxCamera.read()
	cntr = cntr + 1;
	if ((cntr % 30) == 0):

		imgH, imgW,_ = frame.shape
		x1,y1,w1,h1 = 0,0,imgH,imgW

		imgchar = pytesseract.image_to_string(frame)
		
		imgboxes = pytesseract.image_to_boxes(frame)
		for boxes in imgboxes.splitlines():
			boxes = boxes.split(' ')
			x,y,w,h = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
			cv2.rectangle(frame, (x, imgH-y), (w, imgH-h), (0,0,255),3)

		cv2.putText(frame, imgchar, (x1 + int(w1/50), y1 + int(h1/50)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

		font = cv2.FONT_HERSHEY_SIMPLEX
		'''


def cards():
	baxCamera = cv2.VideoCapture(0)

	while True:
		ret, frame = baxCamera.read()

		cv2.imshow('Baxter Camera', frame)

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		options = apriltag.DetectorOptions(families = "tag36h11")
		detector = apriltag.Detector(options)
		results = detector.detect(gray)

		if cv2.waitKey(1) & 0xFF == ord('s'):
			#cv2.imwrite('card.jpg', frame)
			break

	baxCamera.release()
	cv2.destroyAllWindows()

	for r in results:
		tagID = r.tag_id

		print("tagID: {}".format(tagID))

		if (tagID == 0):
			print("Advance to Boardwalk\n")
			break

		elif (tagID == 1):
			print("Advance to Go (Collect $200)\n")
			break	

		elif (tagID == 2):
			print("Get out of Jail Free\n")
			break

		elif (tagID == 3):
			print("Go Back 3 Spaces\n")
			break		

		elif (tagID == 4):
			print("Take a Trip to Reading Railroad. If you pass GO, collect $200.\n")
			break

		elif (tagID == 5):
			print("Doctor's fee. Pay $50.\n")
			break

		elif (tagID == 6):
			print("Advance to Go (Collect $200)\n")
			break




#cardPath = 'card.jpg'
#text = pytesseract.image_to_string(frame.open(cardPath))
#print(text[:-1])

def get_dice(blobs):

	X = []

	for b in blobs:

		pos = b.pt

		if pos != None:
			X.append(pos)


	X = np.asarray(X)

	if len(X) > 0:

		clustering = cluster.DBSCAN(eps=40, min_samples=1).fit(X)

		num_dice = max(clustering.labels_) + 1

		dice = []

		for i in range(num_dice):
			X_dice = X[clustering.labels_ == i]

			centroid_dice = np.mean(X_dice, axis=0)

			dice.append([len(X_dice), *centroid_dice])

		return dice

	else:
		return []

def overlay_info(frame, dice, blobs):

	for b in blobs:
		pos = b.pt

		r = b.size / 2


		cv2.circle(frame, (int(pos[0]), int(pos[1])), int(r), (255, 0, 0), 2)

	for d in dice:

		textsize = cv2.getTextSize(str(d[0]), cv2.FONT_HERSHEY_PLAIN, 3, 2) [0]

		cv2.putText(frame, str(d[0]), (int(d[1] - textsize[0] / 2), int(d[2] + textsize[1] / 2)), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)


def diceRoll():

	baxCamera = cv2.VideoCapture(0)

	params = cv2.SimpleBlobDetector_Params()

	params.filterByArea = True
	params.minArea = 30


	params.filterByCircularity = True
	params.maxCircularity = 1


	params.filterByInertia = True
	params.minInertiaRatio = 0.5
	params.maxInertiaRatio = 1


	while True:
		key = (cv2.waitKey(1) & 0xFF == ord('s'))

		ret, frame = baxCamera.read()



		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		detector = cv2.SimpleBlobDetector_create(params)

		blobs = detector.detect(gray)

		dice = get_dice(blobs)

		out_frame = overlay_info(frame, dice, blobs)



		cv2.imshow('Baxter Camera', frame)
		

		
		if key:
			#cv2.imwrite('card.jpg', frame)
			dice1 = dice[0][0]

			dice2 = dice[1][0]
		
			count = len(blobs)
			break		

	baxCamera.release()
	cv2.destroyAllWindows()


	if (dice1 == dice2):
		print("Doubles!")

	print("Dice Total: " + str(count) + "\n")



def yolov8():
	baxCamera = cv2.VideoCapture(0)

	model = YOLO("Money/money.pt")

	while True:
		ret, frame = baxCamera.read()

		cv2.imshow('Baxter Camera', frame)

		money = model.predict(source=frame)

		if cv2.waitKey(1) & 0xFF == ord('s'):
			#cv2.imwrite('card.jpg', frame)
			break

	

def main():


	userInput = None


	while True:

		print("0: Test Monopoly Cards\n1: Test Dice Roll\n2: Yolo\n3: Exit")

		userInput = input()

		if (userInput == '0'):
			cards()
			break

		elif (userInput == '1'):
			diceRoll()
			

		elif (userInput == '2'):
			yolov8()
			break

		elif (userInput == '3'):
			break



if __name__ == '__main__':
	main()










