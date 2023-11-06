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

# required library
import rospy
from math import cos, sin, pi
# required message types
from sensor_msgs.msg import Joy
from rospy_tutorials.msg import Floats

# global variable:
global robot_movement_array, encoder_value_x, encoder_value_y, encoder_value_x_b, encoder_value_y_b
robot_movement_array = Floats()
robot_movement_array.data = [0.0, 0.0, 0.0, 0.0, 0.0]
encoder_value_x = 0.0
encoder_value_y = 0.0


def callback(msg):
    global encoder_value_x, encoder_value_y, encoder_value_x_b, encoder_value_y_b
    encoder_value_x = msg.data[0]
    encoder_value_y = msg.data[1]
    encoder_value_x_b = msg.data[2]
    encoder_value_y_b = msg.data[3]


def rezero():
    global encoder_value_x, encoder_value_y, encoder_value_x_b, encoder_value_y_b
    rospy.init_node('auto_pub', anonymous=True)
    r = rospy.Rate(30)  # Hz
    amp = 40.0
    pub = rospy.Publisher('/vel_array', Floats, queue_size=1)
    rospy.Subscriber("/motors_states", Floats, callback)
    # print(encoder_value_x, encoder_value_y)
    # block for calling back
    # robot_movement_array.data[0] = 50.0  # amp*sin(2*pi*ros_time/T_frq)
    # robot_movement_array.data[1] = 0.0
    # robot_movement_array.data[2] = 0.0
    # robot_movement_array.data[3] = 0.0
    # robot_movement_array.data[4] = 0.0
    # pub.publish(robot_movement_array)
    rospy.sleep(1)
    ####

    while not rospy.is_shutdown():
        print('test text', encoder_value_x, encoder_value_y)
        while encoder_value_x > 2:
            robot_movement_array.data[0] = amp  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = 0.0
            robot_movement_array.data[2] = 0.0
            robot_movement_array.data[3] = 0.0
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()

        while encoder_value_x < -2:
            robot_movement_array.data[0] = -amp  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = 0.0
            robot_movement_array.data[2] = 0.0
            robot_movement_array.data[3] = 0.0
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()

        while encoder_value_y > 2:
            robot_movement_array.data[0] = 0.0  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = amp
            robot_movement_array.data[2] = 0.0
            robot_movement_array.data[3] = 0.0
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()

        while encoder_value_y < -2:
            robot_movement_array.data[0] = 0.0  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = -amp
            robot_movement_array.data[2] = 0.0
            robot_movement_array.data[3] = 0.0
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()

        while encoder_value_x_b > 2:
            robot_movement_array.data[0] = 0.0  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = 0.0
            robot_movement_array.data[2] = amp
            robot_movement_array.data[3] = 0.0
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()

        while encoder_value_x_b < -2:
            robot_movement_array.data[0] = 0.0  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = 0.0
            robot_movement_array.data[2] = -amp
            robot_movement_array.data[3] = 0.0
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()

        while encoder_value_y_b > 2:
            robot_movement_array.data[0] = 0.0  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = 0.0
            robot_movement_array.data[2] = 0.0
            robot_movement_array.data[3] = amp
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()

        while encoder_value_y_b < -2:
            robot_movement_array.data[0] = 0.0  # amp*sin(2*pi*ros_time/T_frq)
            robot_movement_array.data[1] = 0.0
            robot_movement_array.data[2] = 0.0
            robot_movement_array.data[3] = -amp
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;", robot_movement_array.data[0])
            r.sleep()



        robot_movement_array.data[0] = 0.0
        robot_movement_array.data[1] = 0.0
        robot_movement_array.data[2] = 0.0
        robot_movement_array.data[3] = 0.0
        robot_movement_array.data[4] = 0.0
        pub.publish(robot_movement_array)
        print('final encoder result:', encoder_value_x, encoder_value_y)
        rospy.loginfo(rospy.get_caller_id() + "ROS shutting down, stop all the motor movement")
        rospy.sleep(0.2)
        break


def func_gen(ros_time, freq, amp, function="cos"):
    if function == "cos":
        y = amp * cos(2 * pi * ros_time / freq)
    elif function == "sin":
        y = amp * sin(2 * pi * ros_time / freq)
    else:
        y = 0

    return y


def remap(old_value, old_max=1.0, old_min=-1.0, new_max=3.0, new_min=-3.0):
    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    return new_value


if __name__ == '__main__':
    try:
        rezero()
    except:
        pass
