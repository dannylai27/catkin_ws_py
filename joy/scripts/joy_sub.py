#!/usr/bin/env python3

# sub topic1: /joy, [Joy] 

# Joy.axes[0] --> left joystick, left +1 to right -1
# Joy.axes[1] --> left joystick, down -1 to up    +1
# Joy.axes[2] --> ?
# Joy.axes[3] --> right joystick, left +1 to right -1
# Joy.axes[4] --> right joystick, down -1 to up    +1
# Joy.axes[5] --> ?

#required library
import rospy

#required message types
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
# from rospy_tutorials.msg import Floats


#global variable:
global pub, joy_movement
joy_movement = Float64()
joy_movement.data = [0, 0, 0, 0]



def callback(data):
    global pub
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.axes[1])
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.axes[3])
    joy_movement.data = data.axes[1]
    # message type FloatMultiArray32
    # joy_movement.data[0] = data.axes[0]
    # joy_movement.data[1] = data.axes[1]
    # joy_movement.data[2] = data.axes[3]
    # joy_movement.data[3] = data.axes[4]
    pub.publish(joy_movement)
    
def listener():
    global pub
    rospy.init_node('joy_sub_pub', anonymous=True)
    rospy.Subscriber("/joy", Joy, callback)
    pub = rospy.Publisher('/joy_movement', Float64, queue_size=1)
    rospy.spin()

if __name__ == '__main__':
    listener()
