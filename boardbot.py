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

"""
Author: Adam Hurd (Team 34)
Project: BoardBot
Class: CS425/426

This script is a modifed version of the "ik_pick_and_play_demo.py" by
Rethink Robotics that is supplied with the Baxter SDK.

This script will demonstrate BoardBot's ability to play Monopoly.
Some features may be hardcoded, stubbed, or otherwise mocked-up
pending full implementation. See TODO's/documentation for details.

Acronyms:
IK = inverse kinematics

"""

import argparse 
import struct
import sys
import copy
 
import rospy
import rospkg

from itertools import cycle # used for board traversal

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


class pieceManipulator(object):
	#				  string type	distance is meters	 		Used for debugging
	def __init__(self, limb_arg, hover_distance_arg = 0.25, verbose_output_arg=False):
		self._limb_name = limb_arg 
		self._hover_distance = hover_distance_arg
		self._verbose_output = verbose_output_arg

		# Associate baxter arm/grip controllers with a given limb
		self._limb = baxter_interface.Limb(limb_arg) #
		self._gripper = baxter_interface.Gripper(limb_arg)

		# Set up ROS services
		service_name = "placeManipulator for " + limb_arg
		self._ik_service = rospy.ServiceProxy(service_name, SolvePositionIK)
		rospy.wait_for_service(service_name, 10.0) # wait up to 10 seconds for service

		# Enable robot
		self._robot_state = baxter_interface.RobotEnable(baxter_interface.CHECK_VERSION)
		self._initial_state = self._robot_state.state().enabled
		self._robot_state.enable()
		if self._verbose_output:
			print("Robot is enabled")
		
	# Move the named limb to the ready position
	def move_arm_to_ready(self, arm_name,  start_angles=None):
		if self._verbose_output:
			print("Moving arm ", arm_name, " to the ready position")
		if not start_angles:
			start_angles = dict(zip(self._joint_names, [0]*7))
		
		self._move_arm_to_position(start_angles)
		self.end_effector_open()
		rospy.sleep(1.0) # wait one second before processing next command

	# Given a desired pose (goal), get the IK necessary to acheive it
	def get_IK(self, pose_arg):
		ik_header = Header(current_time=rospy.Time.now(), frame_id='base')
		ik_request = SolvePositionIKRequest()
		ik_request.current_pose.append(Pose(header=ik_header, pose=pose_arg))
		# Send IK request to IK service
		try:
			ik_result = self._ik_service(ik_request)
		except (rospy.ServiceException, rospy.ROSException), e:
			rospy.logerr("Service call failed: %s" % (e,))
			return False
			
		# Verify that ik_result is valid (goal can be reached). Also convert rospy strings to int
		ik_result_seeds = struct.unpack('<%dB' % len(ik_result.result_type, ik_result.result_type)
		limb_joint_goals = {} # positions that joints must achieve to reach goal
		if (ik_result_seeds[0] != ik_result_seeds.RESULT_INVALID):
			seed_struct = { ik_request.SEED_USER: 'User-provided Seed',
							ik_request.SEED_CURRENT: 'Current Joint Angles',
							ik_request.SEED_NS_MAP: 'Nullspace Setpoints', 
						  }.get(ik_result_seeds[0], 'None')
			if self._verbose_output:
				print("Valid IK found - Solution from Seed type: {0}".format(seed_str))

			# Re-format IK solution for Limb API
			limb_joints = dict(zip(ik_result_seeds.joints[0].name, ik_result_seeds.joints[0].position))

			if self._verbose_output:
				print("IK Joint Solution:\n{0}".format(limb_joints))
				print("\n")

		# Invalid ik_result/solution
		else:
			rospy.logerr("INVALID POSE - bad IK solution or none found.")
			return False
		return limb_joints

	def move_arm_to_position(self, joint_angles):
		if joint_angles:
			self._limb.move_to_joint_positions(joint_angles)
		else:
			rospy.logerr("No joint angles provided to move_arm_to_position().")

	def end_effector_open(self):
	# TODO: add code for vacuum cup. This code only works for the standard gripper
	# For vacuum cup, "open" means release vacuum (no suction).
		self._gripper.open()
		rospy.sleep(1.0)

	def end_effector_close(self):
	# TODO: add code for vacuum cup.
	# For vacuum cup, "close" means apply vacuum (suction).
		self._gripper.close()
		rospy.sleep(1.0)

	def _approach(self, pose): 
		approach = copy.deepcopy(pose)
        # approach with a pose the hover-distance above the requested pose
        approach.position.z = approach.position.z + self._hover_distance
        joint_angles = self.get_IK(approach)
        self._move_arm_to_position(joint_angles)

	def _retract(self):
        # retrieve current pose from endpoint
        current_pose = self._limb.endpoint_pose()
        ik_pose = Pose()
        ik_pose.position.x = current_pose['position'].x
        ik_pose.position.y = current_pose['position'].y
        ik_pose.position.z = current_pose['position'].z + self._hover_distance
        ik_pose.orientation.x = current_pose['orientation'].x
        ik_pose.orientation.y = current_pose['orientation'].y
        ik_pose.orientation.z = current_pose['orientation'].z
        ik_pose.orientation.w = current_pose['orientation'].w
        joint_angles = self.ik_request(ik_pose)
        # servo up from current pose
        self._move_arm_to_position(joint_angles)

	# Move servo (end effector)
	def _servo_to_pose(self, pose):
        # servo down to release
        joint_angles = self.ik_request(pose)
        self._move_arm_to_position(joint_angles)

	def pick_up_piece(self, pose):
	# TODO: Test this with the vacuum cup.
		# open the gripper
        self.gripper_open()
        # servo above pose
        self._approach(pose)
        # servo to pose
        self._servo_to_pose(pose)
        # close gripper
        self.gripper_close()
        # retract to clear object
        self._retract()

	def place_piece(self, pose):
	# TODO: Test this with the vacuum cup.
        # servo above pose
        self._approach(pose)
        # servo to pose
        self._servo_to_pose(pose)
        # open the gripper
        self.gripper_open()
        # retract to clear object
        self._retract()

# TODO: Add code/reference for board on the table
def load_gazebo_models(table_pose=Pose(position=Point(x=1.0, y=0.0, z=0.0)),
                       table_reference_frame="world",
                       block_pose=Pose(position=Point(x=0.6725, y=0.1265, z=0.7825)),
                       block_reference_frame="world"):
    # Get Models' Path
    model_path = rospkg.RosPack().get_path('')+"/models/"
    # Load Table SDF
    table_xml = ''
    with open (model_path + "cafe_table/model.sdf", "r") as table_file:
        table_xml=table_file.read().replace('\n', '')
    # Load Block URDF
    block_xml = ''
    with open (model_path + "block/model.urdf", "r") as block_file:
        block_xml=block_file.read().replace('\n', '')
    # Spawn Table SDF
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf("cafe_table", table_xml, "/",
                             table_pose, table_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))
    # Spawn Block URDF
    rospy.wait_for_service('/gazebo/spawn_urdf_model')
    try:
        spawn_urdf = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
        resp_urdf = spawn_urdf("block", block_xml, "/",
                               block_pose, block_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn URDF service call failed: {0}".format(e))

def delete_gazebo_models():
    # This will be called on ROS Exit, deleting Gazebo models
    # Do not wait for the Gazebo Delete Model service, since
    # Gazebo should already be running. If the service is not
    # available since Gazebo has been killed, it is fine to error out
    try:
        delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        resp_delete = delete_model("cafe_table")
        resp_delete = delete_model("block")
    except rospy.ServiceException, e:
        rospy.loginfo("Delete Model service call failed: {0}".format(e))

def main():
	# Create ROS node for this script
	rospy.init_node("boardbot.py")
	
	# Populate gazebo with the appropriate models
	load_gazebo_models()

	# Remove models on shutdown
	rospy.on_shutdown(delete_gazebo_models)

	# wait for ROS to complete startup sequence
	rospy.wait_for_message("/robot/sim/started", Empty)

	# Use left limb (Y-gripper) to move player piece around the board
	limb = 'left'
	hover_distance = 0.1 # 0.1 m or 10 cm
	starting_joint_angles = {'left_w0': 0.6699952259595108,
                             'left_w1': 1.030009435085784,
                             'left_w2': -0.4999997247485215,
                             'left_e0': -1.189968899785275,
                             'left_e1': 1.9400238130755056,
                             'left_s0': -0.08000397926829805,
                             'left_s1': -0.9999781166910306}
	manipulator = pieceManipulator(limb, hover_distance)

	# An orientation for gripper fingers to be overhead and parallel to the obj
    overhead_orientation = Quaternion(
                             x=-0.0249590815779,
                             y=0.999649402929,
                             z=0.00737916180073,
                             w=0.00486450832011)

	# TODO: since the board is static, consider putting this information
	# in another format such as a JSON file, just to keep main() clean
	block_poses = list()

	# Initial space; "GO"
	block_poses.append(Pose(
        position=Point(x=0.7, y=0.0, z=-0.129),
        orientation=overhead_orientation))

	# Move the player piece by 4 cm each time
	block_poses.append(Pose(
        position=Point(x=0.74, y=0.0, z=-0.129),
        orientation=overhead_orientation))

	block_poses.append(Pose(
        position=Point(x=0.78, y=0.0, z=-0.129),
        orientation=overhead_orientation))

	block_poses.append(Pose(
        position=Point(x=0.82, y=0.0, z=-0.129),
        orientation=overhead_orientation))

	block_poses.append(Pose(
        position=Point(x=0.84, y=0.0, z=-0.129),
        orientation=overhead_orientation))

	block_poses.append(Pose(
        position=Point(x=0.88, y=0.0, z=-0.129),
        orientation=overhead_orientation))
	
	manipulator.move_arm_to_ready(starting_joint_angles)
	board_space = 0 # "GO" space

	# Move the piece around the board until the program is terminated
	# TODO: add condition to check for "player turn"
	while not rospy.is_shutdown():
		manipulator.pick_up_piece(block_poses[board_space])

		# go to next space; loop around to "GO" as needed
		board_space = (board_space+1) % len(block_poses) 	

		manipulator.place_piece(block_poses[board_space])
	return 0

if __name__ = '__main__':
	sys.exit(main())
	
	
		
