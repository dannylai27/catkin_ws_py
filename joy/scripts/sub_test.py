#!/usr/bin/env python
# license removed for brevity
import rospy
import cv2 as cv
#to test sub, change to the message you need!
from sensor_msgs.msg import Image
img_message = Image()

def callback(data):
    rospy.loginfo('receive data')

def listener():
    rospy.init_node('sub_test_node', anonymous=True)
    rospy.Subscriber('Naneye_video', Image, callback)
    while not rospy.is_shutdown():
        rospy.spin()
        
        
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
