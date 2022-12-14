# Team34_BoardBot

This project assumes the following installations:

- Ubuntu 18.04, non-VM
- catkin_tools
- ROS-melodic-desktop-full
- Baxter SDK
- Baxter SDK Melodic update: https://github.com/qingchenkanlu/Baxter-SDK/blob/main/Baxter_SDK_Moveit_GazeboSimulator_Melodic.zip
- MoveIt for Melodic: 
```
rosdep update
sudo apt update
sudo apt dist-upgrade
sudo apt install ros-melodic-moveit
```
Note that a dedicated GPU is required to run the simulation software Gazebo and RViz.
All ROS software must be 'melodic' unless specified otherwise.

Asset placement:
- Models: ~/workspace/src/baxter_simulator/baxter_sim_examples
- World files: ~/workspace/src/baxter_simulator/baxter_gazebo/worlds
- Scripts: ~/workspace/src/baxter_simulator/baxter_sim_examples/scripts
- Launch files: ~/workspace/src/baxter_simulator/baxter_gazebo/launch


To run the simulation, open a terminal and enter:
```
cd ~/workspace
catkin_make
source devel/setup.bash
. baxter.sh sim
roslaunch baxter_gazebo baxter_world.launch
```

Wait several moments for gazebo to load; you should see the Baxter robot next to a table with Monopoly

Open another terminal and enter:
```
cd ~/workspace
source devel.setup.bash
rosrun baxter_sim_examples ik_pick_and_place_demo.py
```
You should see the Baxter robot begin to move its arms and execute the demo sequence



