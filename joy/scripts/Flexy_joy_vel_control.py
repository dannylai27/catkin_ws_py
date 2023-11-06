#!/usr/bin/env python3

######################################################

### This script is used to control Flexy_4_stepper_controller_vel_DUE.io!

######################################################
# sub topic1: /joy, [Joy] 

# Joy.axes[0] --> left joystick, left +1 to right -1
# Joy.axes[1] --> left joystick, down -1 to up    +1
# Joy.axes[2] --> L2 analog
# Joy.axes[3] --> right joystick, left +1 to right -1
# Joy.axes[4] --> right joystick, down -1 to up    +1
# Joy.axes[5] --> R2 analog
# Joy.axes[6] --> left panel, Left and Right (1 when left arrow pressed, 0 when released, -1 when right arrow pressed)
# Joy.axes[7] --> left panel, Up and Down (1 when up arrow pressed, 0 when released, -1 when down arrow pressed)

# Joy.buttonx[0] --> X
# Joy.buttonx[1] --> O
# Joy.buttonx[2] --> Triangle
# Joy.buttonx[3] --> Square
# Joy.buttonx[4] --> L1
# Joy.buttonx[5] --> R1
# Joy.buttonx[6] --> L2
# Joy.buttonx[7] --> R2
# Joy.buttonx[8] --> Share
# Joy.buttonx[9] --> PS
# Joy.buttonx[10] --> Options
# Joy.buttonx[11] --> JoyStick Left Press
# Joy.buttonx[12] --> JoyStick Right Press

#required library
import rospy

#required message types
from sensor_msgs.msg import Joy
from rospy_tutorials.msg import Floats


#global variable:
global robot_movement_array, Right_joy_x, Right_joy_y, Left_joy_x, Left_joy_y, scalar
robot_movement_array = Floats()
robot_movement_array.data = [0.0, 0.0, 0.0, 0.0, 0.0]
Right_joy_x = 0.0
Right_joy_y = 0.0
Left_joy_x = 0.0
Left_joy_y = 0.0
scalar = 6.0

def callback(data):
    global Right_joy_x, Right_joy_y, Left_joy_x, Left_joy_y, scalar
    
    Right_joy_x = data.axes[0]
    Right_joy_y = data.axes[1]
    Left_joy_x = data.axes[3]
    Left_joy_y = data.axes[4]
    if scalar > 0:
        scalar = scalar - data.buttons[0]
    if scalar < 12: # 25 is possible ( not reaching max yet) for two motors
        scalar = scalar + data.buttons[2]
   
        
def listener():
    global Right_joy_x, Right_joy_y, Left_joy_x, Left_joy_y, pub, scalar
    rospy.init_node('joy_sub_pub', anonymous=True)
    r = rospy.Rate(30)  # 40 Hz is possible when two motors are running simulaneously
    rospy.Subscriber("/joy", Joy, callback)
    pub = rospy.Publisher('/vel_array', Floats, queue_size=1)

    while not rospy.is_shutdown():
    
        robot_movement_array.data[0] = remap(Right_joy_x, old_max=1.0, old_min=-1.0, new_max=scalar*100, new_min=-scalar*100)
        robot_movement_array.data[1] = remap(Right_joy_y, old_max=1.0, old_min=-1.0, new_max=scalar*100, new_min=-scalar*100)
        robot_movement_array.data[2] = remap(Left_joy_x, old_max=1.0, old_min=-1.0, new_max=scalar*100, new_min=-scalar*100)
        robot_movement_array.data[3] = remap(Left_joy_y, old_max=1.0, old_min=-1.0, new_max=scalar*100, new_min=-scalar*100)
        pub.publish(robot_movement_array)
        rospy.loginfo(rospy.get_caller_id() + "R_x: %s, R_y: %s, L_x: %s, L_y: %s,the button is: %s", robot_movement_array.data[0], robot_movement_array.data[1], robot_movement_array.data[2], robot_movement_array.data[3], scalar)
        r.sleep()
        
    	
    # rospy.spin()

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
    try:
        listener()
    except:
        pass
