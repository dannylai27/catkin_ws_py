#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float32MultiArray
joy_message = Float32MultiArray()

def talker():
    pub = rospy.Publisher('joy_message', Float32MultiArray, queue_size=10)
    rospy.init_node('joy_arduino_node', anonymous=True)
    rate = rospy.Rate(30) # 10hz
    while not rospy.is_shutdown():
        joy_message.data = [float(0.0), float(0.1), float(0.2), float(0.3), float(0.4), float(0.5)]
        rospy.loginfo(joy_message)
        pub.publish(joy_message)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
