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

#pub = rospy.Publisher('diceVals', Int16MultiArray, queue_size=10)

bridge = cv_bridge.CvBridge()

def apTagID(results):
    for r in results:
        tagID = r.tag_id
        
        
    print(tagID)
    return tagID

#Detects april tags and uses tag id to identify monopoly cards.
def cards(ros_img):
    print("Test 1")
#    rospy.sleep(2.0)
#       baxCamera = cv2.VideoCapture(0)

#    bridge = cv_bridge.CvBridge()
    tagID = None

    cv_image1 = bridge.imgmsg_to_cv2(ros_img, desired_encoding="passthrough")
    print("Test 2")
    #       while True:
    #               ret, frame = baxCamera.read()

#while True
#    cv2.imshow('Baxter Camera', cv_image1)   
#    cv2.waitKey(1)

#    gray = cv2.cvtColor(cv_image1, cv2.COLOR_BGR2GRAY)

#    options = apriltag.DetectorOptions(families = "tag36h11")
#    detector = apriltag.Detector(options)
#    results = detector.detect(gray)


    print("Test 3")

    #               if cv2.waitKey(1) & 0xFF == ord('s'):
                    #cv2.imwrite('card.jpg', frame)
    #                       break

    #       baxCamera.release()
    #       cv2.destroyAllWindows()
    
    cv2.imshow('Baxter Camera', cv_image1)   
    cv2.waitKey(1)

    pubID = None
#    while pubID == None:
    


    gray = cv2.cvtColor(cv_image1, cv2.COLOR_BGR2GRAY)

    options = apriltag.DetectorOptions(families = "tag36h11")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    
    print(results)
#        for r in results:
    print("Show Card")
    tagID = apTagID(results)

    print("tagID: {}".format(tagID))

    if (tagID == 0):
            print("Block Party\n")
            pubID = 0
#            break

    elif (tagID == 1):
            print("Animal Shelter\n")
            pubID = 1
            #break   

    elif (tagID == 2):
            print("Bake Sale\n")
            pubID = 2
            #break

    elif (tagID == 3):
            print("Go To Jail.\n")
            pubID = 3
            #break           

    elif (tagID == 4):
            print("Car Wash\n")
            pubID = 4
            #break

    elif (tagID == 5):
            print("Get out of jail\n")
            pubID = 5
            #break

    elif (tagID == 6):
            print("Local Children's Hospital\n")
            pubID = 6
            #break
            
    elif (tagID == 7):
            print("Cleaning Town's Walking path\n")
            pubID = 7
            #break

    elif (tagID == 8):
            print("Home Improvement\n")
            pubID = 8
            #break   

    elif (tagID == 9):
            print("Neighbor groceries\n")
            pubID = 9
            #break

    elif (tagID == 10):
            print("Blood drive\n")
            pubID = 10
            #break
            
    elif (tagID == 11):
            print("Bake Sale buy cookies\n")
            pubID = 11
            #break   

    elif (tagID == 12):
            print("Hang out with elderly neightbor\n")
            pubID = 12
            #break

    elif (tagID == 13):
            print("New School Playground\n")
            pubID = 13
            #break           

    elif (tagID == 14):
            print("Help neighbor clean up\n")
            pubID = 14
            #break

    elif (tagID == 15):
            print("Advance to Go.\n")
            pubID = 15
            #break

    elif (tagID == 16):
            print("Speeding fine\n")
            pubID = 16
            #break
            
    elif (tagID == 17):
            print("Bank pays you dividend of 50\n")
            pubID = 17
            #break

    elif (tagID == 18):
            print("Advance to the next Railroad\n")
            pubID = 18
            #break   

    elif (tagID == 19):
            print("Make General Repairs\n")
            pubID = 19
            #break

    elif (tagID == 20):
            print("Advance to Go\n")
            pubID = 20
            #break
            
    elif (tagID == 21):
            print("Go back three spaces\n")
            pubID = 21
            #break   

    elif (tagID == 22):
            print("Advance to Illnois Avenue\n")
            pubID = 22
            #break

    elif (tagID == 23):
            print("Elected Chairperson of the board\n")
            pubID = 23
            #break           

    elif (tagID == 24):
            print("Advance to St. Charles Place\n")
            pubID = 24
            #break

    elif (tagID == 25):
            print("Go to Jail.\n")
            pubID = 25
            #break

    elif (tagID == 26):
            print("Advance to the nearest Utility\n")
            pubID = 26
            #break
            
    elif (tagID == 27):
            print("Advance to Boardwalk\n")
            pubID = 27
            #break

    elif (tagID == 28):
            print("Take a trip to the Reading Railroad\n")
            pubID = 28
            #break   

    elif (tagID == 29):
            print("Get out of Jail Free\n")
            pubID = 29
            #break

    elif (tagID == 30):
            print("Building loan matures\n")
            pubID = 30
            #break
            
    elif (tagID == 31):
            print("Advance to the next Railroad\n")
            pubID = 31
            #break   

    elif (tagID == 32):
            print("Electric Company\n")
            pubID = 32
            #break

    elif (tagID == 33):
            print("Water Works\n")
            pubID = 33
            #break           

    elif (tagID == 34):
            print("B & O Railroad\n")
            pubID = 34
            #break

    elif (tagID == 35):
            print("Pennsylvania Railroad\n")
            pubID = 35
            #break

    elif (tagID == 36):
            print("Short Line\n")
            pubID = 36
            #break
            
    elif (tagID == 37):
            print("Reading Railroad\n")
            pubID = 37
            #break

    elif (tagID == 38):
            print("Virginia Avenue\n")
            pubID = 38
            #break   

    elif (tagID == 39):
            print("St. Charles Place\n")
            pubID = 39
            #break

    elif (tagID == 40):
            print("States Avenue\n")
            pubID = 40
            #break
            
    elif (tagID == 41):
            print("Oriental Avenue\n")
            pubID = 41
            #break   

    elif (tagID == 42):
            print("Vermont Avenue\n")
            pubID = 42
            #break

    elif (tagID == 43):
            print("Connecticut Avenue\n")
            pubID = 43
            #break           

    elif (tagID == 44):
            print("Mediterranean Avenue\n")
            pubID = 44
            #break

    elif (tagID == 45):
            print("Baltic Avenue\n")
            pubID = 45
            #break

    elif (tagID == 46):
            print("Pacific Avenue\n")
            pubID = 46
            #break
            
    elif (tagID == 47):
            print("North Carolina Avenue\n")
            pubID = 47
            #break

    elif (tagID == 48):
            print("Pennsylvania Avenue\n")
            pubID = 48
            #break   

    elif (tagID == 49):
            print("Atlantic Avenue\n")
            pubID = 49
            #break

    elif (tagID == 50):
            print("Ventnor Avenue\n")
            pubID = 50
            #break
            
    elif (tagID == 51):
            print("Marvin Gardens\n")
            pubID = 51
            #break   

    elif (tagID == 52):
            print("Park Place\n")
            pubID = 52
            #break

    elif (tagID == 53):
            print("Boardwalk\n")
            pubID = 53
            #break           

    elif (tagID == 54):
            print("St. James Place\n")
            pubID = 54
            #break

    elif (tagID == 55):
            print("Tennessee Avenue\n")
            pubID = 55
            #break

    elif (tagID == 56):
            print("New York Avenue\n")
            pubID = 56
            #break
            
    elif (tagID == 57):
            print("Kentucky Avenue\n")
            pubID = 57
            #break

    elif (tagID == 58):
            print("Indiana Avenue\n")
            pubID = 58
            #break   

    elif (tagID == 59):
            print("Illinois Avenue\n")
            pubID = 59
            #break
                    
            

#       r = rospy.Rate(1)
    #while not rospy.is_shutdown():
    
    
#    if (pubID != None):
    pub = rospy.Publisher('mpCards', Int16, queue_size=10)
    rospy.sleep(2.0)
    pub.publish(pubID)
    print("unregister test cards")
#    camera_pub0.unregister()
    rospy.sleep(2.0)
    cv2.destroyAllWindows()
    del cv_image1
    del tagID
    return        
#    cv_image.release()
#    cv2.destroyAllWindows()
#    rospy.wait_for_message("moveState", Int16).data
#    camera_pub.unregister()
#    os.system("rosrun baxter_tools camera_control.py -c left_hand_camera")

#       r.sleep()

#cardPath = 'card.jpg'
#text = pytesseract.image_to_string(frame.open(cardPath))
#print(text[:-1])


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
        #Initlize cv bridge
#    bridge = cv_bridge.CvBridge()
        
    cv_image = bridge.imgmsg_to_cv2(ros_img, desired_encoding="passthrough")

#       baxCamera = cv2.VideoCapture(0)

        #Parameters for blobs
    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 30

    params.filterByCircularity = True
    params.maxCircularity = 1


    params.filterByInertia = True
    params.minInertiaRatio = 0.5
    params.maxInertiaRatio = 1

        
        #while True:

                

#               ret, frame = baxCamera.read()

    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    detector = cv2.SimpleBlobDetector_create(params)

    blobs = detector.detect(gray)

    dice = get_dice(blobs)

    out_frame = overlay_info(cv_image, dice, blobs)


    cv2.imshow('Baxter Camera', cv_image)
                
    cv2.waitKey(1)

#               if key:
                                #cv2.imwrite('card.jpg', frame)
    dice1 = dice[0][0]

    dice2 = dice[1][0]
                
#       count = len(blobs)
#               break           

#       cv_image.release()
#       cv2.destroyAllWindows()
    dices.append(int(dice1))
    dices.append(int(dice2))
        
    diceVals.data = dices

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
                
#       while not rospy.is_shutdown():
#       pub1.publish(diceDoubles)
    publishValue(pub, diceVals)
#    cv_image.release()
    cv2.destroyAllWindows()
#    camera_pub1.unregister()
    rospy.sleep(2.0)
#    del cv_image
#    return
#    os.system("rosrun baxter_tools camera_control.py -c left_hand_camera")


#    r.sleep()
        
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
                        #cv2.imwrite('card.jpg', frame)
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
#        var = (
#            True    
            #False
#            )
        # TODO
#        os.system("rosrun baxter_tools camera_control.py -c head_camera")
#        os.system("rosrun baxter_tools camera_control.py -c right_hand_camera")
        # Open left hand camera
#        os.system("rosrun baxter_tools camera_control.py -o left_hand_camera")
        print("Before wait...")
        global camera_pub1
        var = rospy.wait_for_message("moveState", Int16).data
#        var = 0
        print("After wait")
        print(var)

#        if(var == 0):  
#                camera_pub1.unregister()
 #               print("Cards")      
#                camera_pub0 = rospy.Subscriber('/cameras/left_hand_camera/image', Image, cards)
#                rospy.sleep(2.0)
#                camera_pub0.unregister()
#                del camera_pub0
#                cv2.destroyAllWindows()
#                rospy.wait_for_message('mpCards', Int16)
#                camera_pub.unregister()
                
        if (var == 1):
#                camera_pub0.unregister()
                print("Rolling Dice")
                camera_pub1 = rospy.Subscriber('/cameras/left_hand_camera/image', Image, diceRoll)
                rospy.sleep(2.0)
#                rospy.wait_for_message("diceTotal", Int16MultiArray)
                camera_pub1.unregister()
                del camera_pub1
#                quit()
#                cv2.destroyAllWindows()
#                rospy.wait_for_message('diceVals', Int16MultiArray)
#                camera_pub.unregister()
    #           cvPublisher(dice)       
    
        else:
            print("Invalid moveState message data value")
            
#        camera_pub.unregister()
                
        # Close left hand camera
#        os.system("rosrun baxter_tools camera_control.py -c left_hand_camera")
    return 0
#        rospy.spin()

'''
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
'''


if __name__ == '__main__':
        main()



