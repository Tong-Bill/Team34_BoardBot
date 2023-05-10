#!/usr/bin/env python


import cv2
import numpy as np
import apriltag
import rospy
import cv_bridge
import os
from std_msgs.msg import Int16
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from ultralytics import YOLO
from sklearn import cluster

#Initlize cv bridge
bridge = cv_bridge.CvBridge()

def apTagID(results):
    for r in results:
        tagID = r.tag_id
        
        
    print(tagID)
    return tagID

#Detects april tags and uses tag id to identify monopoly cards.
def cards(ros_img):

    tagID = None

    cv_image1 = bridge.imgmsg_to_cv2(ros_img, desired_encoding="passthrough")

    #Displays camera feed to computer screen for testing purposes
    cv2.imshow('Baxter Camera', cv_image1)   
    cv2.waitKey(1)

    pubID = None
    

    gray = cv2.cvtColor(cv_image1, cv2.COLOR_BGR2GRAY)

    options = apriltag.DetectorOptions(families = "tag36h11")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    

    print("Show Card")
    tagID = apTagID(results)

    print("tagID: {}".format(tagID))

    if (tagID == 0):
            print("Block Party\n")
            pubID = 0
            

    elif (tagID == 1):
            print("Animal Shelter\n")
            pubID = 1
                   

    elif (tagID == 2):
            print("Bake Sale\n")
            pubID = 2
            

    elif (tagID == 3):
            print("Go To Jail.\n")
            pubID = 3
                       

    elif (tagID == 4):
            print("Car Wash\n")
            pubID = 4
            

    elif (tagID == 5):
            print("Get out of jail\n")
            pubID = 5
           

    elif (tagID == 6):
            print("Local Children's Hospital\n")
            pubID = 6
           
            
    elif (tagID == 7):
            print("Cleaning Town's Walking path\n")
            pubID = 7
           

    elif (tagID == 8):
            print("Home Improvement\n")
            pubID = 8
              

    elif (tagID == 9):
            print("Neighbor groceries\n")
            pubID = 9
           

    elif (tagID == 10):
            print("Blood drive\n")
            pubID = 10
           
            
    elif (tagID == 11):
            print("Bake Sale buy cookies\n")
            pubID = 11
              

    elif (tagID == 12):
            print("Hang out with elderly neightbor\n")
            pubID = 12
           

    elif (tagID == 13):
            print("New School Playground\n")
            pubID = 13
                      

    elif (tagID == 14):
            print("Help neighbor clean up\n")
            pubID = 14
           

    elif (tagID == 15):
            print("Advance to Go.\n")
            pubID = 15
           

    elif (tagID == 16):
            print("Speeding fine\n")
            pubID = 16
           
            
    elif (tagID == 17):
            print("Bank pays you dividend of 50\n")
            pubID = 17
           

    elif (tagID == 18):
            print("Advance to the next Railroad\n")
            pubID = 18
              

    elif (tagID == 19):
            print("Make General Repairs\n")
            pubID = 19
           

    elif (tagID == 20):
            print("Advance to Go\n")
            pubID = 20
           
            
    elif (tagID == 21):
            print("Go back three spaces\n")
            pubID = 21
              

    elif (tagID == 22):
            print("Advance to Illnois Avenue\n")
            pubID = 22
           

    elif (tagID == 23):
            print("Elected Chairperson of the board\n")
            pubID = 23
                      

    elif (tagID == 24):
            print("Advance to St. Charles Place\n")
            pubID = 24
           

    elif (tagID == 25):
            print("Go to Jail.\n")
            pubID = 25
            

    elif (tagID == 26):
            print("Advance to the nearest Utility\n")
            pubID = 26
            
            
    elif (tagID == 27):
            print("Advance to Boardwalk\n")
            pubID = 27
            

    elif (tagID == 28):
            print("Take a trip to the Reading Railroad\n")
            pubID = 28
               

    elif (tagID == 29):
            print("Get out of Jail Free\n")
            pubID = 29
            

    elif (tagID == 30):
            print("Building loan matures\n")
            pubID = 30
            
            
    elif (tagID == 31):
            print("Advance to the next Railroad\n")
            pubID = 31
               

    elif (tagID == 32):
            print("Electric Company\n")
            pubID = 32
            

    elif (tagID == 33):
            print("Water Works\n")
            pubID = 33
                       

    elif (tagID == 34):
            print("B & O Railroad\n")
            pubID = 34
            

    elif (tagID == 35):
            print("Pennsylvania Railroad\n")
            pubID = 35
            

    elif (tagID == 36):
            print("Short Line\n")
            pubID = 36
            
            
    elif (tagID == 37):
            print("Reading Railroad\n")
            pubID = 37
            

    elif (tagID == 38):
            print("Virginia Avenue\n")
            pubID = 38
               

    elif (tagID == 39):
            print("St. Charles Place\n")
            pubID = 39
            

    elif (tagID == 40):
            print("States Avenue\n")
            pubID = 40
            
            
    elif (tagID == 41):
            print("Oriental Avenue\n")
            pubID = 41
               

    elif (tagID == 42):
            print("Vermont Avenue\n")
            pubID = 42
            

    elif (tagID == 43):
            print("Connecticut Avenue\n")
            pubID = 43
                       

    elif (tagID == 44):
            print("Mediterranean Avenue\n")
            pubID = 44
            

    elif (tagID == 45):
            print("Baltic Avenue\n")
            pubID = 45
            

    elif (tagID == 46):
            print("Pacific Avenue\n")
            pubID = 46
            
            
    elif (tagID == 47):
            print("North Carolina Avenue\n")
            pubID = 47
            

    elif (tagID == 48):
            print("Pennsylvania Avenue\n")
            pubID = 48
               

    elif (tagID == 49):
            print("Atlantic Avenue\n")
            pubID = 49
            

    elif (tagID == 50):
            print("Ventnor Avenue\n")
            pubID = 50
            
            
    elif (tagID == 51):
            print("Marvin Gardens\n")
            pubID = 51
               

    elif (tagID == 52):
            print("Park Place\n")
            pubID = 52
            

    elif (tagID == 53):
            print("Boardwalk\n")
            pubID = 53
                       

    elif (tagID == 54):
            print("St. James Place\n")
            pubID = 54
            

    elif (tagID == 55):
            print("Tennessee Avenue\n")
            pubID = 55
            

    elif (tagID == 56):
            print("New York Avenue\n")
            pubID = 56
            
            
    elif (tagID == 57):
            print("Kentucky Avenue\n")
            pubID = 57
            

    elif (tagID == 58):
            print("Indiana Avenue\n")
            pubID = 58
               

    elif (tagID == 59):
            print("Illinois Avenue\n")
            pubID = 59
            
                    
            


    pub = rospy.Publisher('mpCards', Int16, queue_size=10)
    rospy.sleep(2.0)
    pub.publish(pubID)
    print("unregister test cards")
    rospy.sleep(2.0)
    cv2.destroyAllWindows()
    del cv_image1
    return        



#Code used from Quentin Golsteyn at https://golsteyn.com/writing/dice
#Function for detecting individual dice
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

#Code used from Quentin Golsteyn at https://golsteyn.com/writing/dice
#Puts text and colored dots on dice in camera feed
def overlay_info(frame, dice, blobs):

        for b in blobs:
                pos = b.pt

                r = b.size / 2


                cv2.circle(frame, (int(pos[0]), int(pos[1])), int(r), (255, 0, 0), 2)

        for d in dice:

                textsize = cv2.getTextSize(str(d[0]), cv2.FONT_HERSHEY_PLAIN, 3, 2) [0]

                cv2.putText(frame, str(d[0]), (int(d[1] - textsize[0] / 2), int(d[2] + textsize[1] / 2)), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

#Detects dice roll, counts total and if dice are doubles.
def diceRoll(ros_img):
    pub = rospy.Publisher('diceVals', Int16MultiArray, queue_size=10)
    diceVals = Int16MultiArray()
    dices = []

        
    cv_image = bridge.imgmsg_to_cv2(ros_img, desired_encoding="passthrough")


    #Parameters for blobs
    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 30

    params.filterByCircularity = True
    params.maxCircularity = 1


    params.filterByInertia = True
    params.minInertiaRatio = 0.5
    params.maxInertiaRatio = 1


    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    detector = cv2.SimpleBlobDetector_create(params)

    blobs = detector.detect(gray)

    dice = get_dice(blobs)

    out_frame = overlay_info(cv_image, dice, blobs)

    #Displays camera feed to computer screen for testing purposes
    cv2.imshow('Baxter Camera', cv_image)
                
    cv2.waitKey(1)

    dice1 = dice[0][0]

    dice2 = dice[1][0]
                

    dices.append(int(dice1))
    dices.append(int(dice2))
        

    diceVals.data = dices

#Recognizes doubles
#       if (dice1 == dice2):
#               diceDoubles = True
#               print("\nDoubles!")
#       else:
#               diceDoubles = False
#               print("\nNot doubles.")

#       diceTotal = count
#       print("Dice Total: " + str(count) + "\n")
#       print(diceDoubles)
#       print(diceTotal)
        
#       pub1 = rospy.Publisher('diceDoubles', Bool, queue_size=10)

#    r = rospy.Rate(1)
                

    publishValue(pub, diceVals)

    cv2.destroyAllWindows()

    rospy.sleep(2.0)


        
def publishValue(pub, diceVals):
    pub.publish(diceVals)       

#Yolo function to detect monopoly money
def yolov8():
        baxCamera = cv2.VideoCapture(0)

        model = YOLO("Money/money.pt")

        while True:
                ret, frame = baxCamera.read()

                cv2.imshow('Baxter Camera', frame)

                money = model.predict(source=frame)

                if cv2.waitKey(1) & 0xFF == ord('s'):
                        break

        
def cvPublisher(dice):
        global diceDoubles
        global diceTotal

        pub2 = rospy.Publisher('diceTotal', Int16MultiArray, queue_size=10)

        r = rospy.Rate(1)
        while not rospy.is_shutdown():
                pub2.publish(diceTotal)
                r.sleep()


def main():
    print("Main start")
    rospy.init_node('baxter_cv')
    global camera_pub0
    
    while not rospy.is_shutdown():

        print("Before wait...")
        global camera_pub1
        var = rospy.wait_for_message("moveState", Int16).data
        print("After wait")
        print(var)

       if(var == 0):  
                print("Cards")      
                camera_pub0 = rospy.Subscriber('/cameras/left_hand_camera/image', Image, cards)
                rospy.sleep(2.0)

                
        if (var == 1):
                print("Rolling Dice")
                camera_pub1 = rospy.Subscriber('/cameras/left_hand_camera/image', Image, diceRoll)
                rospy.sleep(2.0)
      
    
        else:
            print("Invalid moveState message data value")
            

    return 0



if __name__ == '__main__':
        main()



