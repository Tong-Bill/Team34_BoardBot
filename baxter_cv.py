#from imutils.object_detection import non_max_suppression
#import pytesseract
#import argparse
import cv2
import numpy as np
import apriltag

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

		if cv2.waitKey(2) & 0xFF == ord('s'):
			#cv2.imwrite('card.jpg', frame)
			#baxCamera.release()
			cv2.destroyAllWindows()
			break

	for r in results:
		tagID = r.tag_id

		print("tagID: {}".format(tagID))

		if (tagID == 0):
			print("Advance to Boardwalk")
			break

		elif (tagID == 1):
			print("Advance to Go (Collect $200)")
			break	

		elif (tagID == 2):
			print("Get out of Jail Free")
			break

		elif (tagID == 3):
			print("Go Back 3 Spaces")
			break		

		elif (tagID == 4):
			print("Take a Trip to Reading Railroad. If you pass GO, collect $200.")
			break

		elif (tagID == 5):
			print("Doctor's fee. Pay $50.")
			break

		elif (tagID == 6):
			print("Advance to Go (Collect $200)")
			break



#cardPath = 'card.jpg'
#text = pytesseract.image_to_string(frame.open(cardPath))
#print(text[:-1])

def diceRoll():

	baxCamera = cv2.VideoCapture(0)

	params = cv2.SimpleBlobDetector_Params()

	params.filterByArea = True
	params.minArea = 100

	params.filterByCircularity = True
	params.minConvexity = 0.2

	params.filterByInertia = True 
	params.minInertiaRatio = 0.01


	while True:
		ret, frame = baxCamera.read()

		cv2.imshow('Baxter Camera', frame)

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		detector = cv2.SimpleBlobDetector_create(params)

		blobs = detector.detect(gray)
		
		count = len(blobs)
		
		if cv2.waitKey(2) & 0xFF == ord('s'):
			#cv2.imwrite('card.jpg', frame)
			break		

	print("Dice Number: " + str(count))


def main():
	print("0: Test Monopoly Cards\n1: Test Dice Roll\n2: Exit")

	userInput = None

	while (userInput != '2'):

		userInput = input()

		if (userInput == '0'):
			cards()

		elif (userInput == '1'):
			diceRoll()

		elif (userInput == '2'):
			break

	quit()
if __name__ == '__main__':
	main()










