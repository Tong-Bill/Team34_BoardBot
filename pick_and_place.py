#!/usr/bin/env python

# Copyright (c) 2013-2015, Rethink Robotics
# All rights reserved.

""" 
Team 34: BoardBot
Jacob Boe
"""


"""
Baxter RSDK Inverse Kinematics Pick and Place Demo
"""
dice_roll = 0 #global

import argparse
import struct
import sys
import copy
import os

import rospy
import rospkg

import numpy as np
import PyKDL

import rospy
import baxter_interface

from baxter_interface import gripper as robot_gripper
from std_msgs.msg import (Int16, String,)
from baxter_kdl.kdl_parser import kdl_tree_from_urdf_model
from urdf_parser_py.urdf import URDF

from gazebo_msgs.srv import (
        SpawnModel,
        DeleteModel,
)
from geometry_msgs.msg import (
        PoseStamped,
        Pose,
        Point,
        Quaternion,
)
from std_msgs.msg import (
        Header,
        Empty,
)

from baxter_core_msgs.srv import (
        SolvePositionIK,
        SolvePositionIKRequest,
)

import baxter_interface

#class PickAndPlace():
class PickAndPlace(object):
        def __init__(self, limb, hover_distance = 0.15, verbose=True):
                self._limb_name = limb # string
                self._hover_distance = hover_distance # in meters
                self._limb = baxter_interface.Limb(limb)
                self._gripper = robot_gripper.Gripper(limb)
                ns = "ExternalTools/" + limb + "/PositionKinematicsNode/IKService"
                print("Getting robot state... ")
                self._rs = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
                self._init_state = self._rs.state().enabled
                print("Enabling robot... ")
                self._rs.enable()
        
                self._baxter = URDF.from_parameter_server(key='robot_description')
                self._kdl_tree = kdl_tree_from_urdf_model(self._baxter)
                self._base_link = self._baxter.get_root()
                self._tip_link = limb + '_gripper'
                self._tip_frame = PyKDL.Frame()
                self._arm_chain = self._kdl_tree.getChain(self._base_link,
                                                  self._tip_link)

        # Baxter Interface Limb Instances
                self._limb_interface = baxter_interface.Limb(limb)
                self._joint_names = self._limb_interface.joint_names()
                self._num_jnts = len(self._joint_names)

        # KDL Solvers
                self._fk_p_kdl = PyKDL.ChainFkSolverPos_recursive(self._arm_chain)
                self._fk_v_kdl = PyKDL.ChainFkSolverVel_recursive(self._arm_chain)
                self._ik_v_kdl = PyKDL.ChainIkSolverVel_pinv(self._arm_chain)
                self._ik_p_kdl = PyKDL.ChainIkSolverPos_NR(self._arm_chain,
                                                   self._fk_p_kdl,
                                                   self._ik_v_kdl)
                self._jac_kdl = PyKDL.ChainJntToJacSolver(self._arm_chain)
                self._dyn_kdl = PyKDL.ChainDynParam(self._arm_chain,
                                            PyKDL.Vector.Zero())
                                            
        def inverse_kinematics(self, position, orientation, seed=None):
                ik = PyKDL.ChainIkSolverVel_pinv(self._arm_chain)
                pos = PyKDL.Vector(position[0], position[1], position[2])
                if orientation != None:
                        rot = PyKDL.Rotation()
                        rot = rot.Quaternion(orientation[0], orientation[1], orientation[2], orientation[3])
        # Populate seed with current angles if not provided
                seed_array = PyKDL.JntArray(self._num_jnts)
                if seed != None:
                        seed_array.resize(len(seed))
                        for idx, jnt in enumerate(seed):
                                seed_array[idx] = jnt
                else:
                        seed_array = self.joints_to_kdl('positions')

        # Make IK Call
                if orientation:
                        goal_pose = PyKDL.Frame(rot, pos)
                else:
                        goal_pose = PyKDL.Frame(pos)
                result_angles = PyKDL.JntArray(self._num_jnts)

                if self._ik_p_kdl.CartToJnt(seed_array, goal_pose, result_angles) >= 0:
                        result = dict(zip(self._joint_names, result_angles))
                        return result
                else:
                        return None
           
        def joints_to_kdl(self, type, values=None):
                kdl_array = PyKDL.JntArray(self._num_jnts)

                if values is None:
                        if type == 'positions':
                                cur_type_values = self._limb_interface.joint_angles()
                        elif type == 'velocities':
                                cur_type_values = self._limb_interface.joint_velocities()
                        elif type == 'torques':
                                cur_type_values = self._limb_interface.joint_efforts()
                else:
                        cur_type_values = values
        
                for idx, name in enumerate(self._joint_names):
                        kdl_array[idx] = cur_type_values[name]
                if type == 'velocities':
                        kdl_array = PyKDL.JntArrayVel(kdl_array)
                return kdl_array
                
        def move_to_start(self, start_angles=None):
                print("Moving the {0} arm to start pose...".format(self._limb_name))
                if not start_angles:
                        start_angles = dict(zip(self._joint_names, [0]*7))
                self._guarded_move_to_joint_position(start_angles)
                self.gripper_open()
                rospy.sleep(1.0)
                print("Running. Ctrl-c to quit")
                
        def move(self, start_angles=None):
                print("Moving the {0} arm to start pose...".format(self._limb_name))
                if not start_angles:
                        start_angles = dict(zip(self._joint_names, [0]*7))
                self._guarded_move_to_joint_position(start_angles)
                self.gripper_close()
                rospy.sleep(1.0)
                print("Running. Ctrl-c to quit")

        def _guarded_move_to_joint_position(self, joint_angles):
                try:
                        if len(joint_angles) > 1:
                                self._limb.move_to_joint_positions(joint_angles)
                        else:
                                rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")
                except:
                        rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")

        def gripper_open(self):
                self._gripper.open()
                rospy.sleep(1.0)

        def gripper_close(self):
                self._gripper.close()
                rospy.sleep(1.0)
                
        def gripper_calibrate(self):
        	self._gripper.calibrate()
        	rospy.sleep(2.0)

        def _approach(self, pos1, rot):
                posT = copy.deepcopy(pos1)
                rotT = copy.deepcopy(rot)
        # approach with a pose the hover-distance above the requested pose
                posT[2] = posT[2] + self._hover_distance
                joint_angles = self.inverse_kinematics(posT, rotT)
                print(joint_angles)
                self._guarded_move_to_joint_position(joint_angles)

        def _retract(self):
        # retrieve current pose from endpoint
                current_pose = self._limb.endpoint_pose()
                pos = [0, 0, 0]
                rot = [0, 0, 0, 0]
                ik_pose = Pose()
                pos[0] = current_pose['position'].x
                pos[1] = current_pose['position'].y
                pos[2] = current_pose['position'].z + self._hover_distance
                rot[0] = current_pose['orientation'].x
                rot[1] = current_pose['orientation'].y
                rot[2] = current_pose['orientation'].z
                rot[3] = current_pose['orientation'].w
                joint_angles = self.inverse_kinematics(pos, rot)
        # servo up from current pose
                self._guarded_move_to_joint_position(joint_angles)

        def _servo_to_pose(self, pos, rot):
        # servo down to release
                joint_angles = self.inverse_kinematics(pos, rot)
                self._guarded_move_to_joint_position(joint_angles)

        def pick(self, pos1, rot, pos_test=None):
        # open the gripper
                self.gripper_open()
        # servo above pose
                self._approach(pos1, rot)
        # servo to pose
                self._servo_to_pose(pos1, rot)
        # close gripper
                self.gripper_close()
                if pos_test == None:
        # retract to clear object
                    self._retract()
                else:
                    self.move(pos_test)

        def place(self, pos2, rot, pos_test=None):
        # servo above pose
                self._approach(pos2, rot)
        # servo to pose
                self._servo_to_pose(pos2, rot)
        # open the gripper
                self.gripper_open()
                if pos_test == None:
        # retract to clear object
                    self._retract()
                else:
                    self.move_to_start(pos_test)
        
        def roll_dice(self, pos_dice, pos_roll, rot):
            # Publisher to tell when movements are done   
            pub = rospy.Publisher("moveState", Int16, queue_size=10) 
    # open the gripper
            self.gripper_open()
    # servo above pose
            self._approach(pos_dice, rot)
    # servo to pose
            self._servo_to_pose(pos_dice, rot)
    # close gripper
            self.gripper_close()
    # retract to clear object
            self._retract()
    # servo above pose
            self._approach(pos_roll, rot)
    # servo to pose
            self._servo_to_pose(pos_roll, rot)
    # open the gripper
            self.gripper_open()
            temp_roll = copy.deepcopy(pos_roll) 
            temp_roll[2] = -0.06
    # servo above pose
            self._approach(temp_roll, rot)
    # servo to pose
            self._servo_to_pose(temp_roll, rot)
            pub.publish(1)
  
def get_position(count, dice_roll, board_space):
        for i in range(dice_roll):
                count += 1
                if count >= 40:
                        count -= 40
 #                       board_space = ([0.474062, 0.4, 0.0])
                        board_space = ([0.474062, 0.4, -0.08])
                elif count == 1 or count == 10:
                        board_space[0] += .048
                elif count == 11 or count == 20:
                        board_space[1] -= .048
                elif count == 21 or count == 30:
                        board_space[0] -= .048
                elif count == 31:
                        board_space[1] += .048
                elif count > 1 and count < 10:
                        board_space[0] += .042
                elif count > 11 and count < 20:
                        board_space[1] -= .042
                elif count > 21 and count < 30:
                        board_space[0] -= .042
                elif count > 31 and count < 40:
                        board_space[1] += .042
            
        return board_space	


# Test function for verifying PubSub setup
def callback(data):
    global dice_roll 
    dice_roll = data.data
        #print("\n\nI got stuff!\n\n")

# Subscriber function: gets space information from AI
def subscribeSpace(board_spaces, rot, pnp, count_start, count_finish, dice_roll, pub, joint_angles):
#    global dice_roll
#    rospy.Subscriber("spaceInfo", Int16, callback) # Topic: spaceInfo; get message, then invoke 'callback()'
    print("Dice_roll is:\n")
    print(dice_roll)
    count_finish += dice_roll
    if count_finish >= 40:
        count_finish -= 40
    # 31 - 39
    if count_start <= 7 or count_start >= 26:
        if count_start >= 31 and count_start <= 39:
            pnp.pick(board_spaces[count_start], rot, joint_angles[0])
        else:
            pnp.pick(board_spaces[count_start], rot)
    else:
        pnp.move_to_start(joint_angles[0])
        pnp.move(joint_angles[count_start])
        pnp.move(joint_angles[0])
        
    if count_finish <= 7 or count_finish >= 26:
        if count_finish >= 30 and count_finish <= 39:
            pnp.place(board_spaces[count_finish], rot, joint_angles[0])
        else:
            pnp.place(board_spaces[count_finish], rot)
    else:
        pnp.move_to_start(joint_angles[count_finish])
        pnp.move_to_start(joint_angles[0])
    
#    pnp.pick(board_spaces[count_start], rot)  # Pick up at origin
#    board_space = get_position(count, dice_roll, board_space) # Calc destination
#    count += dice_roll  
#    pnp.place(board_spaces[count_finish], rot) # Go to destination
    pub.publish(2)
    # Keep instance running to receive more messages
    return count_finish


def diceRollCallback(data, pnp):
    dice_space = ([0.64, 0.3, -0.085])
    roll_space = ([0.692725, 0.181337, 0.22])
    rot = [-0.0249590815779, 0.999649402929, 0.00737916180073, 0.00486450832011]
    
    if data.data == 1:
        pnp.roll_dice(dice_space, roll_space, rot)
        data.data = 0



def main():
    # Subscribe to spaceMovement
    rospy.init_node('spaceMovement') 
    pub = rospy.Publisher("moveState", Int16, queue_size=10) 

    limb = 'left'
    hover_distance = 0.15 # meters
    
    # Starting Joint angles for left arm
    starting_joint_angles = {'left_w0': 0.6699952259595108,
                            'left_w1': 1.030009435085784,
                            'left_w2': -0.4999997247485215,
                            'left_e0': -1.189968899785275,
                            'left_e1': 1.9400238130755056,
                            'left_s0': -0.08000397926829805,
                            'left_s1': -0.9999781166910306}
                            
    # Read cards joint angles
    cards_joint_angles = {'left_w0': -0.17602429520874024,
                            'left_w1': -1.3192234760742187,
                            'left_w2': 0.08245146725463867,
                            'left_e0': -0.2308641083129883,
                            'left_e1': 2.2415294237365724,
                            'left_s0': -0.8314175860839844,
                            'left_s1': -0.7942185520202637}
                            
    board_spaces = { 0: [0.474062, 0.4, -0.08],
                    1: [.524062, .4, -.08],
                    2: [.565062, .4, -.08],
                    3: [.606062, .4, -.08],
                    4: [.647062, .4, -.08],
                    5: [.688062, .4, -.08],
                    6: [.729062, .4, -.08],
                    7: [.770062, .4, -.08],
                    23: [.74, -.045, -.08],
                    24: [7, -.045, -.08],
                    25: [.645, -.045, -.08],
                    26: [.62, -.045, -.08],
                    27: [.58, -.045, -.08],
                    28: [.54, -.045, -.08],
                    29: [.49, -.045, -.08],
                    30: [.435, -.03, -.08],
                    31: [.435, .025, -.08],
                    32: [.435, .07, -.08],
                    33: [.445, .111, -.08],
                    34: [.445, .152, -.08],
                    35: [.445, .193, -.08],
                    36: [.445, .234, -.08],
                    37: [.455, .274, -.08],
                    38: [.455, .315, -.08],
                    39: [.46, .333, -.08]
                    }
    
    joint_angles = { 0: {'left_w0': 0.6699952259595108,
                            'left_w1': 1.030009435085784,
                            'left_w2': -0.4999997247485215,
                            'left_e0': -1.189968899785275,
                            'left_e1': 1.9400238130755056,
                            'left_s0': -0.08000397926829805,
                            'left_s1': -0.9999781166910306},
                    8: {'left_w0': -0.18791264630126955, 
                            'left_w1': 0.7957525328063966,
                            'left_w2': 0.26231071442871096, 
                            'left_e0': 0.22357769957885743, 
                            'left_e1': 0.9974710061828614, 
                            'left_s0': -0.7558690323669434, 
                            'left_s1': -0.3160000419433594},
                    9: {'left_w0': -0.15493205939941407, 
                            'left_w1': 0.7006457240661621,
                            'left_w2': 0.15301458341674806, 
                            'left_e0': 0.1580000209716797, 
                            'left_e1': 0.945699154650879, 
                            'left_s0': -0.7090826183898926, 
                            'left_s1': -0.2922233397583008},
                    10: {'left_w0': -0.1100631214050293, 
                            'left_w1': 0.6784030026672364,
                            'left_w2': 0.17372332402954102, 
                            'left_e0': 0.09587379913330078, 
                            'left_e1': 0.8291166149047852, 
                            'left_s0': -0.6849224210083008, 
                            'left_s1': -0.24236896420898438},
                    11: {'left_w0': 0.3347913065734863, 
                            'left_w1': 1.0036069293273926,
                            'left_w2': 0.021092235809326173, 
                            'left_e0': -0.2895388733825684, 
                            'left_e1': 0.39039811007080083, 
                            'left_s0': -0.6396699878173828, 
                            'left_s1': -0.03758252926025391},
                    12: {'left_w0': 0.30794664281616213, 
                            'left_w1': 0.9729273136047364,
                            'left_w2': 0.05675728908691407, 
                            'left_e0': -0.23661653626098633, 
                            'left_e1': 0.49739326990356447, 
                            'left_s0': -0.6895243633666993, 
                            'left_s1': -0.08245146725463867},
                    13: {'left_w0': 0.27611654150390624, 
                            'left_w1': 0.804189427130127,
                            'left_w2': -0.13307283319702148, 
                            'left_e0': -0.11236409258422853, 
                            'left_e1': 0.7620049555114746, 
                            'left_s0': -0.7949855424133301, 
                            'left_s1': -0.20823789171752932},
                    14: {'left_w0': 0.26614566639404297, 
                            'left_w1': 0.783480686517334,
                            'left_w2': -0.16106798254394533, 
                            'left_e0': -0.08935438079223633, 
                            'left_e1': 0.7351602917541504, 
                            'left_s0': -0.8624806970031739, 
                            'left_s1': -0.1928980838562012},
                    15: {'left_w0': 0.241601973815918, 
                            'left_w1': 0.7869321432861328,
                            'left_w2': -0.1695048768676758, 
                            'left_e0': -0.10354370306396485, 
                            'left_e1': 0.7370777677368164, 
                            'left_s0': -0.8862573991882324, 
                            'left_s1': -0.19596604542846682},
                    16: {'left_w0': 0.11274758778076173, 
                            'left_w1': 0.698344752886963,
                            'left_w2': -0.2546408104980469, 
                            'left_e0': 0.015339807861328126, 
                            'left_e1': 0.7892331144653321, 
                            'left_s0': -0.9859661502868653, 
                            'left_s1': -0.21322332927246096},
                    17: {'left_w0': 0.10584467424316407, 
                            'left_w1': 0.7014127144592286,
                            'left_w2': -0.23661653626098633, 
                            'left_e0': 0.03067961572265625, 
                            'left_e1': 0.783480686517334, 
                            'left_s0': -1.0461748961425783, 
                            'left_s1': -0.2078543965209961},
                    18: {'left_w0': 0.05675728908691407, 
                            'left_w1': 0.6791699930603028,
                            'left_w2': -0.31906800351562503, 
                            'left_e0': 0.07516505852050782, 
                            'left_e1': 0.7838641817138673, 
                            'left_s0': -1.1201894690734864, 
                            'left_s1': -0.1948155598388672},
                    19: {'left_w0': 0.004985437554931641, 
                            'left_w1': 0.6047719249328614,
                            'left_w2': -0.2937573205444336, 
                            'left_e0': 0.11389807337036134, 
                            'left_e1': 0.8030389415405274, 
                            'left_s0': -1.1819321957153321, 
                            'left_s1': -0.1940485694458008},
                    20: {'left_w0': 0.14802914586181642, 
                            'left_w1': 0.6481068821411133,
                            'left_w2': -0.19213109346313478, 
                            'left_e0': -0.03988350043945313, 
                            'left_e1': 0.7090826183898926, 
                            'left_s0': -1.1627574358886719, 
                            'left_s1': -0.15186409782714844},
                    21: {'left_w0': 0.6181942568115235, 
                            'left_w1': 1.0143447948303224,
                            'left_w2': -0.41800976422119146, 
                            'left_e0': -0.4513738463195801, 
                            'left_e1': 0.5000777362792969, 
                            'left_s0': -1.0803059686340333, 
                            'left_s1': -0.03758252926025391},
                    22: {'left_w0': 0.6231796943664552, 
                            'left_w1': 0.8632476873962402,
                            'left_w2': -0.5522330830078125, 
                            'left_e0': -0.45635928387451175, 
                            'left_e1': 0.8421554515869141, 
                            'left_s0': -0.996704015789795, 
                            'left_s1': -0.1844611895324707},
                    23: {'left_w0': 0.5660389100830079, 
                            'left_w1': 1.0273836315124512,
                            'left_w2': -0.5522330830078125, 
                            'left_e0': -0.4368010288513184, 
                            'left_e1': 0.7896166096618653, 
                            'left_s0': -1.043873924963379, 
                            'left_s1': -0.1710388576538086},                 
                    24: {'left_w0': 0.4042039371459961, 
                            'left_w1': 0.8521263266967773,
                            'left_w2': -0.5633544437072754, 
                            'left_e0': -0.2972087773132324, 
                            'left_e1': 1.0668836367553711, 
                            'left_s0': -1.0730195598999024, 
                            'left_s1': -0.3160000419433594},               
                    25: {'left_w0': 0.39538354762573247, 
                            'left_w1': 0.8018884559509278,
                            'left_w2': -0.6458059109619141 , 
                            'left_e0': -0.2707476087524414, 
                            'left_e1': 1.2172137537963867, 
                            'left_s0': -1.0952622812988282, 
                            'left_s1': -0.37314082622680667}}
                                                                                                                     
    # Starting Joint angles for left arm
    starting_joint_angles = {'left_w0': 0.6699952259595108,
                            'left_w1': 1.030009435085784,
                            'left_w2': -0.4999997247485215,
                            'left_e0': -1.189968899785275,
                            'left_e1': 1.9400238130755056,
                            'left_s0': -0.08000397926829805,
                            'left_s1': -0.9999781166910306}
                          
    # An orientation for gripper fingers to be overhead and parallel to the obj
    rot = [-0.0249590815779, 0.999649402929, 0.00737916180073, 0.00486450832011]
                            
    pnp = PickAndPlace(limb, hover_distance)
    pnp.gripper_calibrate()

    # Starting board space
    board_space = ([0.474062, 0.4, -0.09]) # Go
    dice_space = ([0.64, 0.3, -0.09])
    roll_space = ([0.68, 0.19, 0.22])
    count_start = 0
    count_finish = 0
    
    # "moveState" message values to be published
    #os.system("rosrun baxter_tools baxter_cv.py")
    card_done = 0 # Movement for card reading position finished
    roll_done = 1 # Movement for rolling dice finished
    piece_done = 2 # Movement for moving player piece finished

# Move to the desired starting angles
    pnp.move_to_start(starting_joint_angles)
    
# While running, waits for a new message each loop, then runs code once received
    while not rospy.is_shutdown():
        print("Waiting!\n")
        #value = rospy.wait_for_message("diceRoll", Int16)
        value = rospy.wait_for_message("diceRoll", Int16).data
        print("\n\npick and place got diceRoll!")
        print(value)
    # Waits for integer that is 0 or not 0. 0: roll dice. Otherwise: 
        if value == 0:
            pnp.roll_dice(dice_space, roll_space, rot)
        elif value == 13:
            pnp.move_to_start(cards_joint_angles)
            pub.publish(0)
        elif value == 14:
            pnp.move_to_start(starting_joint_angles)
        else:
            count_start = subscribeSpace(board_spaces, rot, pnp, count_start, count_finish, value, pub, joint_angles)
            count_finish = count_start
    return 0

if __name__ == '__main__':
        sys.exit(main())
