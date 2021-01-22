#!/usr/bin/env python
#imports
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import matplotlib.pyplot as plt


class TakePicture(object):
    def __init__(self):
        #we subscribe to the rgb camera image
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.bridge_object = CvBridge()

    def camera_callback(self,data):
        try:
            # We select bgr8 because its the OpenCV encoding by default
            #we convert the img_sensor msg to cv2 image with the bridge
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
        #the picture is saved in the repository and showed
        cv2.imwrite('/home/user/catkin_ws/src/can.jpg',cv_image)
        cv2.imshow('image',cv_image)  

        cv2.waitKey(1)

#main function
def main():

    #call to the class
    take_picture_object = TakePicture()

    #node initialization
    rospy.init_node('take_picture_node', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
#call to the main() function
if __name__ == '__main__':
    main()
