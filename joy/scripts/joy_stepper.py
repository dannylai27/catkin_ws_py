#!/usr/bin/env python3

######################################################

### This script is used to control Linear_stage!

### TO DO 2022/07/27: Check the remap message from joy

### TO DO 2022/07/27: build the linear_stage.io

######################################################

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
global stepper_speed
stepper_speed = Float64()
stepper_speed.data = 0.0

def callback(data):
    global stepper_speed
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.axes[3])
    stepper_speed.data = remap(data.axes[4], new_max=11999.0, new_min=-11999.0)

def listener():
    global stepper_speed
    rospy.init_node('joy_sub_pub', anonymous=True)
    r = rospy.Rate(240) # 10hz
    rospy.Subscriber("/joy", Joy, callback)
    pub_stepper = rospy.Publisher('/stepper_speed', Float64, queue_size=1)
    while not rospy.is_shutdown():
        pub_stepper.publish(stepper_speed)
        rospy.loginfo(rospy.get_caller_id() + " stepper speed is: %s", stepper_speed.data )
        r.sleep()
        

def remap(old_value, old_max=1.0, old_min=-1.0, new_max=3.0, new_min=-3.0):
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    return new_value
    
def descretize_remap(old_value, threshold=0.5, step=0.001):

    if old_value > 0.0:
        if old_value > threshold:
            new_value = step * 2.0
        else:
            new_value = step
    elif old_value < 0.0:
        if old_value < -threshold:
            new_value = -step * 2.0
        else:
            new_value = -step
    else:
        new_value = 0.0
    
    return new_value
    

if __name__ == '__main__':
    listener()
