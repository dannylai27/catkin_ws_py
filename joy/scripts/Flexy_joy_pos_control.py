#!/usr/bin/env python3

# sub topic1: /joy, [Joy] 

# Joy.axes[0] --> left joystick, left +1 to right -1
# Joy.axes[1] --> left joystick, down -1 to up    +1
# Joy.axes[2] --> L2 analog
# Joy.axes[3] --> right joystick, left +1 to right -1
# Joy.axes[4] --> right joystick, down -1 to up    +1
# Joy.axes[5] --> R2 analog

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
from std_msgs.msg import Float64
# from rospy_tutorials.msg import Floats


#global variable:
global pub_x, pub_y, robot_movement_x, robot_movement_y, step_x, step_y, joy_x, joy_y, joy_x_old, joy_y_old, button
step_x = 0.0
step_y = 0.0
robot_movement_x = Float64()
robot_movement_y = Float64()
robot_movement_x.data = 0.0
robot_movement_y.data = 0.0
joy_x = 0.0
joy_y = 0.0
joy_x_old = 0.0
joy_y_old = 0.0
button = 0

# robot_movement.data = [0, 0, 0, 0]



def callback(data):
    global pub_x, pub_y, step_x, step_y, joy_x, joy_y, joy_x_old, joy_y_old, button
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.axes[3])
    # robot_movement_x.data = remap(data.axes[0])
    # robot_movement_y.data = remap(-data.axes[1])
    
    
    # joy_x = descretize_remap(data.axes[0])
    # joy_y = descretize_remap(-data.axes[1])
    
    joy_x = remap(data.axes[0], old_max=1.0, old_min=-1.0, new_max=0.004, new_min=-0.004)
    joy_y = remap(-data.axes[1], old_max=1.0, old_min=-1.0, new_max=0.004, new_min=-0.004)
    joy_x_old = joy_x
    joy_y_old = joy_y
    
    button = data.buttons[0]
   
    # message type FloatMultiArray32
    # robot_movement.data[0] = data.axes[0]
    # robot_movement.data[1] = data.axes[1]
    # robot_movement.data[2] = data.axes[3]
    # robot_movement.data[3] = data.axes[4]
        
def listener():
    global pub_x, pub_y, button
    rospy.init_node('joy_sub_pub', anonymous=True)
    r = rospy.Rate(60) # 10hz
    rospy.Subscriber("/joy", Joy, callback)
    pub_x = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)
    pub_y = rospy.Publisher('/single_joint_actuator/joint2_position_controller/command', Float64, queue_size=1)
    while not rospy.is_shutdown():
        if button == 0:
            if joy_x > 0.0:
                if joy_x_old < 0.0:
                    robot_movement_x.data = robot_movement_x.data + joy_x + 0.025
                else: 
                    robot_movement_x.data = robot_movement_x.data + joy_x
            elif joy_x < 0.0:
                if joy_x_old > 0.0:
                    robot_movement_x.data = robot_movement_x.data + joy_x - 0.025
                else:
                    robot_movement_x.data = robot_movement_x.data + joy_x
            elif joy_x == 0.0:
                robot_movement_x.data = robot_movement_x.data
            else:
                pass
            
            if joy_y > 0.0:
                if joy_y_old < 0.0:
                    robot_movement_y.data = robot_movement_y.data + joy_y + 0.015
                else: 
                    robot_movement_y.data = robot_movement_y.data + joy_y
            elif joy_y < 0.0:
                if joy_y_old > 0.0:
                    robot_movement_y.data = robot_movement_y.data + joy_y - 0.015
                else:
                    robot_movement_y.data = robot_movement_y.data + joy_y
            elif joy_y == 0.0:
                robot_movement_y.data = robot_movement_y.data
            else:
                pass
            print('normal state ...')
        elif button == 1:
            robot_movement_x.data = 0
            robot_movement_y.data = 0
            print('reset robot position, please wait...')
        
    
        pub_x.publish(robot_movement_x)
        pub_y.publish(robot_movement_y)
        rospy.loginfo(rospy.get_caller_id() + "   I pub x: %s, y: %s, the button is: %s", robot_movement_x.data, robot_movement_y.data, button)
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
    listener()
