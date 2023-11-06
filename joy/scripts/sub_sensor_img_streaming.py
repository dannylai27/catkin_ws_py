#!/usr/bin/env python3
# license removed for brevity
import rospy
import cv2 as cv
import numpy as np
#to test sub, change to the message you need!
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
img_message = Image()

global bridge, cv_img
cv_img = np.zeros((1,1,3))

def callback(data):
    global bridge, cv_img
    rospy.loginfo('receive data')
    cv_img = bridge.imgmsg_to_cv2(data, "rgb8")
    

def listener():
    global bridge, cv_img
    bridge = CvBridge()
    rospy.init_node('streaming_Naneye_node', anonymous=True)
    rospy.Subscriber('/Naneye_video', Image, callback)
    while not rospy.is_shutdown():
        cv.imshow('naneye_video', cv_img)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
        
        
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
