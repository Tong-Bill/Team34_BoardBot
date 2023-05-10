# Author: Bill Tong
# Objective: Loop through emotions on Baxter display
# Used for demonstration of old faces, deprecated in favor of individual emotion bash script from the emotions folder

source /home/bill/baxterws/devel/setup.bash

rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/image1.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/thinking1.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/excited.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/thinking2.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/happy.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/sad.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/neutral.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/ecstatic.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/unhappy.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/surprised.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/wink.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/confused.png;
sleep 3
rosrun baxter_sim_examples xdisplay_image.py --file=`rospack find baxter_sim_examples`/photos/dead.png;





