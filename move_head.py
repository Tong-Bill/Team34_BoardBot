#!/usr/bin/env python

# Copyright (c) 2013-2015, Rethink Robotics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Rethink Robotics nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#Wyatt Young
#Team 34
#Edited and added to rethink robotics head movement example.


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
        
        		
        		

