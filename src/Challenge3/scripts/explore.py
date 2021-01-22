#! /usr/bin/env python

import rospy
import math
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler


roll = 0.0
pitch = 0.0
yaw = 0.0
distance_front = 0
distance_side_g = 0
distance_side_d = 0
state = 0

def callback_odometry(msg):
    global roll, pitch, yaw 
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)


def callback_laser(msg):
    global distance_front
    global distance_side_g
    global distance_side_d
    distance_front = filter(lambda x: x <= 0.5, msg.ranges[328:382])
    distance_side_g = msg.ranges[1]
    distance_side_d = msg.ranges[719]



def follow_wall():
    global yaw
    velocity.linear.x = 0
    velocity.angular.z = 0
    pub_vel.publish(velocity)
    #while target-yaw > 0.1:
    #    velocity.angular.z = kP*(target-yaw)
    #    pub_vel.publish(velocity)
    #    print(target+yaw)
    
def foward():
    velocity.linear.x = 0.5
    velocity.angular.z = 0
    pub_vel.publish(velocity)


rospy.init_node('explore')
pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(1)
target = 90 * math.pi/180 #conversion en radian
velocity = Twist()

kP = 0.5

sub_odom = rospy.Subscriber('/odom', Odometry, callback_odometry)
sub_laser = rospy.Subscriber('/scan', LaserScan, callback_laser)


def convert_degree_to_rad(speed_deg, angle_deg):
       angular_speed_r = speed_deg * 3.14 / 180
       angle_r = angle_deg * 3.14 / 180
       return [angular_speed_r, angle_r]


def rotate():
    global velocity
    # Initialisation
    velocity.linear.x = 0
    velocity.linear.y = 0
    velocity.linear.z = 0
    velocity.angular.x = 0
    velocity.angular.y = 0
    # Conversion de la vitesse et l'angle (en deg) en rad
    speed_d, angle_d = (2, 90)
    angle_r = convert_degree_to_rad(speed_d, angle_d)
    #Sens de la rotation
    velocity.angular.z = -(angle_r[0])  

    t0 = rospy.Time.now().secs
    current_angle = 0
    
    while (current_angle < angle_r[1]):
        pub_vel.publish(velocity)
        t1 = rospy.Time.now().secs
        print(current_angle, angle_r[1])
        current_angle = angle_r[0] * (t1 - t0)
        rate.sleep()

    #Stop
    velocity.linear.x = 0.0
    velocity.angular.z = 0.0


while not rospy.is_shutdown():

    if distance_front:
        velocity.linear.x = 0
        velocity.angular.z = 0.5

    if not distance_front:
    #    if distance_side_g > 0.3:
    #        rotate()

        velocity.linear.x = 0.5
        velocity.angular.z = 0

    print(velocity.linear.x)
    pub_vel.publish(velocity)

    rate.sleep()


