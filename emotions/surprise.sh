# Author: Bill Tong
# Purpose: executes the xdisplay_image script, changing baxter display to the surprise face

source /home/team34/ros_ws/devel/setup.bash

rosrun baxter_tools xdisplay_image.py --file=`rospack find baxter_tools`/images/SurpriseNEOrange.jpg;
