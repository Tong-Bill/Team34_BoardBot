# Author: Bill Tong
# Purpose: executes the xdisplay_image script, changing baxter display to the sad face

source /home/bill/ros_ws/devel/setup.bash

rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/images/SadSWBlue.jpg;

