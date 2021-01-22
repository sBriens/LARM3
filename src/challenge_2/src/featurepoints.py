#!/usr/bin/env python

#Imports
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import matplotlib.pyplot as plt
from std_msgs.msg import String


#global variable which will be used later
depth_image=0
#state variable which gives inforation about the detection of the can
state=0

#this class will initialize the callbacks and the vision algorithm
class LoadFeature(object):
  
    #the __init__ function will subsribe to the rgb and depth camera image
    def __init__(self):

        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.bridge_object = CvBridge()
        self.x = 10
        rospy.Subscriber("/camera/depth/image_raw", Image, self.callback)

    #this is the callback of the depth camera subscriber
    def callback(self, depth_img):
        
        #we will use the global variable depth_image, and transform it into the depth_image and transform it to cv2 image thanks to the bridge
        global depth_image
        depth_image = self.bridge_object.imgmsg_to_cv2(depth_img, desired_encoding="32FC1")
        
    #this is the callback for the rgb image subscriber       
    def camera_callback(self,data):
        
        try:
            # We select bgr8 because its the OpenCV encoding by default
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
            

        except CvBridgeError as e:
            print(e)
        
        #the image_1 corresponds to the can image that we recover with the l_takepicture.launch file
        image_1 = cv2.imread('/home/user/catkin_ws/src/challenge_2/src/can.jpg',1)
        #the image_2 is the image that the rgb camera of the turtlebot is sending
        image_2 = cv_image
    
        #Conversion to gray images
        gray_1 = cv2.cvtColor(image_1, cv2.COLOR_RGB2GRAY)
        gray_2 = cv2.cvtColor(image_2, cv2.COLOR_RGB2GRAY)

        #Initialize the ORB Feature detector
        orb = cv2.ORB_create(nfeatures = 1000)
        
        #Copy of images that will be helpful later
        preview_1 = np.copy(image_1)
        preview_2 = np.copy(image_2)
        dots = np.copy(image_1)

        #keypoints and descriptors of both pictures are provided by the ORB algorithm
        train_keypoints, train_descriptor = orb.detectAndCompute(gray_1, None)
        test_keypoints, test_descriptor = orb.detectAndCompute(gray_2, None)

        #the keypoints of the referenced can are shown with two different style for the dots
        cv2.drawKeypoints(image_1, train_keypoints, preview_1, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.drawKeypoints(image_1, train_keypoints, dots, flags=2)

        #the bf matcher is initialized
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
        
        #A try function is used to test to match the descriptors of the two pictures, if there is no match, the except returns that no can is detected
        try :
            
            matches=bf.match(train_descriptor, test_descriptor)
            #the matches are then sorted out by distance (the shortest the best the descriptor is)
            matches = sorted(matches, key = lambda x : x.distance)
         
            
            #Regardind previous tests, a value of 8 matches has been chosen to prove that the can is a fake or not. If there are more than 8 matches, it is a can, otherwise we can't tell.
            if len(matches)<=8:
                global state
                #state update
                if state!=1:
                    print('not sur if its a can or something else, the robot must get closer')
                    state=1
        
            if len(matches)>8:
                global state
                if state!=2:
                    
                    print('can detected')
                    state=2
                
                #Now that we know that a can has been detected, we defined the good_matches as the ten closest ones
                good_matches = matches[:self.x]
        
                #We convert the keypoints to array in order to be able to read those data
                train_points = np.float32([train_keypoints[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
                test_points = np.float32([test_keypoints[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)
                
                #We will now work on those matches, in order to determine in the more precise way the center of the can, we will first calculate the gravity center of those keypoints
                a=0
                b=0
                L=len(test_points)
                for i in range (0,L):
                    a=a+test_points[i][0][0]
                    b=b+test_points[i][0][1]
                #A and B corresponds respectively to the x and y axis of the gravity center
                A=a/L
                B=b/L
                
                #Now we will find the homography between the keypoints of the pictures to establish a bounding box
                M, mask = cv2.findHomography(train_points, test_points, cv2.RANSAC,5.0)
                
                #the height and width of the referenced can
                h,w = gray_1.shape[:2]
                
                #data conversion
                pts = np.float32([[0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                
                #perspectivetransform is used to have a bounding box which takes into account the perspective of the environment
                dst = cv2.perspectiveTransform(pts,M)
                
                #We will draw the matches between the keypoints of both picture to see
                dots = cv2.drawMatches(dots,train_keypoints,image_2,test_keypoints,good_matches, None,flags=2)
                
                #this will display the bounding_box of the can
                result = cv2.polylines(image_2, [np.int32(dst)], True, (50,0,255),3, cv2.LINE_AA)
       
                #data conversion
                A = A.astype(int)
                B = B.astype(int)
        
                #this distance is the distance from the center of the robot to the gravity center of the can
                dist=depth_image[A,B]
                
                rate=rospy.Rate(1)

                #the publisher is implemented and the distance is published     
                pub= rospy.Publisher('/bottle', String, queue_size=1)
                pub.publish('la bouteille se trouve a ' + str(dist) + ' m du centre du robot')
                rate.sleep()
                #All the imshow to see how the algorithm is working (the imshow will only appear if keypoints are detected)
                cv2.imshow('result', result)
            cv2.imshow('key_points',preview_1)
            cv2.imshow('Detection',image_2)
            cv2.imshow('matches_lines', dots)
                
            cv2.waitKey(1)

        #the except function from earlier 
        except :
            global state
            if state!=0:
                print('no can detected')
                state =0
#main function        
def main():
    
    #call to the class we built
    load_feature_object = LoadFeature()

    #node initialization
    rospy.init_node('feature_node', anonymous=True)
        
    try:
        #to keep the detection going
        rospy.spin()

    #if we want to interrupt the algorithm
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

#call to the main() function
if __name__ == '__main__':
    main()



