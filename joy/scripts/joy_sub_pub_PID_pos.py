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
global pub_x, pub_y, joy_movement_x, joy_movement_y
joy_movement_x = Float64()
joy_movement_y = Float64()
# joy_movement.data = [0, 0, 0, 0]



def callback(data):
    global pub_x, pub_y
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.axes[3])
    joy_movement_x.data = remap(data.axes[0])
    joy_movement_y.data = remap(-data.axes[1])
    # message type FloatMultiArray32
    # joy_movement.data[0] = data.axes[0]
    # joy_movement.data[1] = data.axes[1]
    # joy_movement.data[2] = data.axes[3]
    # joy_movement.data[3] = data.axes[4]
    rospy.loginfo(rospy.get_caller_id() + "   I pub x: %s, y: %s", joy_movement_x.data, joy_movement_y.data )
    pub_x.publish(joy_movement_x)
    pub_y.publish(joy_movement_y)
    
def listener():
    global pub_x, pub_y
    rospy.init_node('joy_sub_pub', anonymous=True)
    rospy.Subscriber("/joy", Joy, callback)
    pub_x = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)
    pub_y = rospy.Publisher('/single_joint_actuator/joint2_position_controller/command', Float64, queue_size=1)
    rospy.spin()

def remap(old_value, old_max=1.0, old_min=-1.0, new_max=3.0, new_min=-3.0):
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((old_value - old_min)*new_range) / old_range) + new_min
    return new_value
    

if __name__ == '__main__':
    listener()
