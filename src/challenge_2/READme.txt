In a terminal, the challenge-2 launch configuration must be launched : roslaunch larm challenge-2.launch.

Then in another terminal the launch file mapping.launch must be launched : roslaunch challenge_2 mapping.launch.

This launch file contains the slam_gmapping node that will help to build the map when the turtlebot moves. Also, rviz must be launched to see the map building during the moves of the robot. 

The launch file also contains the detection algorithm, this algo will print that a can is detected or not, or possibly. It will also display view of the camera of the turtlebot and the feature_matching algorithms applied to the rgb camera of the turtlebot( those views can be acces through the graphical tools).

Finally, this node will publish into the /bottle topic, that can be acces by : rostopic echo /bottle, the distance between the center of the robot and the detected can.
