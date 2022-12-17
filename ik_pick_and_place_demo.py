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
Team 34: BoardBot
This file is based on the pick-and-play demo. Modified by Jacob Boe to use PyKDL instead of the IKSolver package (broken) and incorporate moving around the Monopoly board.
"""


"""
Baxter RSDK Inverse Kinematics Pick and Place Demo
"""
import argparse
import struct
import sys
import copy

import rospy
import rospkg

import numpy as np
import PyKDL

import rospy

import baxter_interface

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

class PickAndPlace(object):
	def __init__(self, limb, hover_distance = 0.15, verbose=True):
		self._limb_name = limb # string
		self._hover_distance = hover_distance # in meters
		self._limb = baxter_interface.Limb(limb)
		self._gripper = baxter_interface.Gripper(limb)
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

	def _guarded_move_to_joint_position(self, joint_angles):
		if len(joint_angles) > 1:
				self._limb.move_to_joint_positions(joint_angles)
		else:
			rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")

	def gripper_open(self):
		self._gripper.open()
		rospy.sleep(1.0)

	def gripper_close(self):
		self._gripper.close()
		rospy.sleep(1.0)

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
		print(current_pose)
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

	def pick(self, pos1, rot):
        # open the gripper
		self.gripper_open()
        # servo above pose
		self._approach(pos1, rot)
        # servo to pose
		self._servo_to_pose(pos1, rot)
        # close gripper
		self.gripper_close()
        # retract to clear object
		self._retract()

	def place(self, pos2, rot):
        # servo above pose
		self._approach(pos2, rot)
        # servo to pose
		self._servo_to_pose(pos2, rot)
        # open the gripper
		self.gripper_open()
        # retract to clear object
		self._retract()

def load_gazebo_models(table_pose=Pose(position=Point(x=1.0, y=0.0, z=0.0)),
                       table_reference_frame="world",
                       monopoly_pose=Pose(position=Point(x=1.0, y=0.0, z=0.7825)),
                       monopoly_reference_frame="world",
                       redDie_pose=Pose(position=Point(x=1.01, y=-0.28, z=0.79)),
                       redDie_reference_frame="world",
                       tophat_pose=Pose(position=Point(x=0.468, y=0.363, z=0.784)),
                       tophat_reference_frame="world"):
    # Get Models' Path
    model_path = rospkg.RosPack().get_path('baxter_sim_examples')+"/models/"

    # Load Table SDF
    table_xml = ''
    with open (model_path + "cafe_table/model.sdf", "r") as table_file:
        table_xml=table_file.read().replace('\n', '')

    # Load Monopoly SDF
    monopoly_xml = ''
    with open (model_path + "monopoly/model.sdf", "r") as monopoly_file:
        monopoly_xml=monopoly_file.read().replace('\n', '') 

    # Load RedDie SDF
    redDie_xml = ''
    with open (model_path + "redDie/model.sdf", "r") as redDie_file:
        redDie_xml=redDie_file.read().replace('\n', '') 

    # Load Tophat SDF
    tophat_xml = ''
    with open (model_path + "tophat/model.sdf", "r") as tophat_file:
        tophat_xml=tophat_file.read().replace('\n', '') 


    # Spawn Table SDF
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf("cafe_table", table_xml, "/",
                             table_pose, table_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))

    # Spawn Monopoly SDF
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf("monopoly", monopoly_xml, "/",
                             monopoly_pose, monopoly_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))

    # Spawn RedDie SDF
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf("redDie", redDie_xml, "/",
                             redDie_pose, redDie_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))

    # Spawn Tophat SDF
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf("tophat", tophat_xml, "/",
                             tophat_pose, tophat_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))

def delete_gazebo_models():
    # This will be called on ROS Exit, deleting Gazebo models
    # Do not wait for the Gazebo Delete Model service, since
    # Gazebo should already be running. If the service is not
    # available since Gazebo has been killed, it is fine to error out
    try:
        delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        resp_delete = delete_model("cafe_table")
        resp_delete = delete_model("monopoly")
        resp_delete = delete_model("redDie")
        resp_delete = delete_model("tophat")
    except rospy.ServiceException, e:
        rospy.loginfo("Delete Model service call failed: {0}".format(e))

def main():
	rospy.init_node("ik_pick_and_place_demo")
    # Load Gazebo Models via Spawning Services
    # Note that the models reference is the /world frame
    # and the IK operates with respect to the /base frame
	load_gazebo_models()
    # Remove models from the scene on shutdown
	rospy.on_shutdown(delete_gazebo_models)

    # Wait for the All Clear from emulator startup
	rospy.wait_for_message("/robot/sim/started", Empty)

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
	pnp = PickAndPlace(limb, hover_distance)
    # An orientation for gripper fingers to be overhead and parallel to the obj
	rot = [-0.0249590815779, 0.999649402929, 0.00737916180073, 0.00486450832011]

	# Starting board space
	board_space = ([0.468, 0.363, -0.14]) # Go
	count = 0
    
    # Move to the desired starting angles
	pnp.move_to_start(starting_joint_angles)
    
    # Move around the monopoly board space by space
	while not rospy.is_shutdown():
		pnp.pick(board_space, rot) 
        # count += <dice roll>  
		count += 1
		if count >= 40:
			count -= 40
			board_space = ([0.468, 0.363, -0.14])
		elif count == 1 or count == 10:
			board_space[0] += .095
		elif count == 11 or count == 20:
			board_space[1] -= .095
		elif count == 21 or count == 30:
			board_space[0] -= .095
		elif count == 31:
			board_space[1] += .095
		elif count > 1 and count < 10:
			board_space[0] += .07
		elif count > 11 and count < 20:
			board_space[1] -= .07
		elif count > 21 and count < 30:
			board_space[0] -= .07
		elif count > 31 and count < 40:
			board_space[1] += .07
		
		pnp.place(board_space, rot)
  
	return 0

if __name__ == '__main__':
    sys.exit(main())
