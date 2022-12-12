#!/usr/bin/env python

#Wyatt Young
#Team 34
#Reference taken from rethink robotics head movement example.


import argparse
import rospy
import os
import baxter_interface
from baxter_interface import CHECK_VERSION
from itertools import cycle

class moveHead(object):
    def __init__(self):
        """
        Moves the head
        """
        self._done = False
        self._head = baxter_interface.Head()

        print("Getting robot state... ")
        self._rs = baxter_interface.RobotEnable(CHECK_VERSION)
        self._init_state = self._rs.state().enabled
        print("Enabling robot... ")
        self._rs.enable()
        print("Running. Ctrl-c to quit")

    def clean_shutdown(self):
        print("\nExiting ...")
        if self._done:
            self.pan_neutral()
        if not self._init_state and self._rs.state().enabled:
            print("Disabling robot...")
            self._rs.disable()

    def pan_neutral(self):
        self._head.set_pan(0.0)

    def head_nod_state(self):
        print(self._head.nodding())


    def disappointment(self):
        self.pan_neutral()

        print("Being disappointed...")

        os.system("rosrun baxter_examples xdisplay_image.py --file=/home/wyatty/ros_ws/src/Baxter_SDK_Moveit_GazeboSimulator_Melodic/baxter_melodic/baxter_examples/share/images/gerty_unhappy.png")    

        self._head.command_nod()
        print("Nodding head... ")

        command_rate = rospy.Rate(1)
        control_rate = rospy.Rate(100)
        start = rospy.get_time()
        
        angle_list = iter([-1.0, 1.0, -1.0, 1.0])

        print("Panning head... ")
        for i in range(4):
            angle = next(angle_list)
            print(angle)
            while (not rospy.is_shutdown() and
                   not (abs(self._head.pan() - angle) <=
                       baxter_interface.HEAD_PAN_ANGLE_TOLERANCE)):
                self._head.set_pan(angle, speed=0.3, timeout=0)
                control_rate.sleep()
            command_rate.sleep()
        	
        self._done = True
        rospy.signal_shutdown("Done being disappointed.")
        		
        		
def main():
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class = arg_fmt, description = main.__doc__)
		
    parser.parse_args(rospy.myargv()[1:])
		
    print("Initializing node...")
    rospy.init_node("rsdk_move_head") 		
        		
    socialize = moveHead()
        
    rospy.on_shutdown(socialize.clean_shutdown)
    print("Socializing... ")
    socialize.disappointment()
    print("Done.")
        
if __name__ == '__main__':
    main()       
        
        		
        		

