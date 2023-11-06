#!/usr/bin/env python
import rospy
from rospy_tutorials.msg import Floats

def my_callback(msg):
    print(msg.data[4])


def test_arduino():
    rospy.init_node('arduino_test') #initialzing the node with name "subscriber_py"
    rospy.Subscriber("/encoder_stepper", Floats, my_callback, queue_size=2)
    rospy.spin() 

if __name__ == '__main__':
    try:
        test_arduino()
    except rospy.ROSInterruptException:
        pass
