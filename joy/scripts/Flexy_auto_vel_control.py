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
from math import cos, sin, pi, exp
# required message types
from sensor_msgs.msg import Joy
from rospy_tutorials.msg import Floats

# global variable:
global robot_movement_array
robot_movement_array = Floats()
robot_movement_array.data = [0.0, 0.0, 0.0, 0.0, 0.0]


def talker():
    rospy.init_node('auto_pub', anonymous=True)
    r = rospy.Rate(35)  # Hz
    amp = 350.0  # 400/500/600/800
    T_frq = 7  # 8/10/12/16
    frq_const = 0.15  # this is used to change the period for experiments
    # f = 1 / (T_frq * frq_const)
    f = 2 * pi / (T_frq * frq_const)
    phase_shift = 6 * T_frq * frq_const / 8
    time_const = 0.2
    # T_frq * frq_const is the real Period!
    pub = rospy.Publisher('/vel_array', Floats, queue_size=1)
    rospy.sleep(1)
    init_time = rospy.get_time()
    while not rospy.is_shutdown():
        now = init_time
        ros_time = now - init_time
        i = 0
        while ros_time < 4 * T_frq * frq_const:
            if i != 0:
                ros_time = now - init_time
            # ros_time = 0
            # robot_movement_array.data[0] = exp(-time_const * ros_time)*(time_const * sin(f*ros_time) + 1 - f *
            # cos(f*ros_time))
            robot_movement_array.data[0] = 0.0
            robot_movement_array.data[1] = 0.0
            # robot_movement_array.data[2] = func_gen_attenuated_center(ros_time, amp, time_const, f)
            robot_movement_array.data[2] = -func_gen_attenuated_side(ros_time, amp, time_const, f, phase_shift)
            # robot_movement_array.data[2] = func_gen_sine_phase_shift(ros_time, amp, frq_const, T_frq)

            # robot_movement_array.data[2] = -amp * exp(-time_const * ros_time) * (
            #         time_const * sin(f * (ros_time + phase_shift)) - f * cos(
            #     f * (ros_time + phase_shift)) + time_const)
            # robot_movement_array.data[2] = (amp / frq_const) * sin(
            #     (2 * pi / (T_frq * frq_const)) * (ros_time + (T_frq * frq_const) / 4))

            # robot_movement_array.data[2] = amp*exp(-time_const*ros_time)*(f*cos(f*ros_time)-sin(f*ros_time))

            # robot_movement_array.data[2] = -amp * exp(-time_const * ros_time) * (
            #              time_const * sin(f * ros_time) - f * cos(f * ros_time) + time_const)
            robot_movement_array.data[3] = 0.0
            robot_movement_array.data[4] = 0.0
            pub.publish(robot_movement_array)
            rospy.loginfo(rospy.get_caller_id() + "  velocity value: %s;  rostime: %s, i = %s",
                          robot_movement_array.data[0],
                          ros_time,
                          i)

            # robot_movement_array.data[1] = amp*exp(-time_const*ros_time)*(f*cos(f*ros_time)-sin(f*ros_time))
            # robot_movement_array.data[2] = (amp / frq_const) * sin(
            #     (2 * pi / (T_frq * frq_const)) * (ros_time + (T_frq * frq_const) / 4))
            # robot_movement_array.data[2] = -amp * exp(-time_const * ros_time) * (
            #         time_const * sin(f * (ros_time + phase_shift)) - f * cos(
            #     f * (ros_time + phase_shift)) + time_const)

            i += 1
            r.sleep()
            now = rospy.get_time()

        robot_movement_array.data[0] = 0.0
        robot_movement_array.data[1] = 0.0
        robot_movement_array.data[2] = 0.0
        robot_movement_array.data[3] = 0.0
        robot_movement_array.data[4] = 0.0
        pub.publish(robot_movement_array)
        rospy.loginfo(rospy.get_caller_id() + "ROS shutting down, stop all the motor movement")
        rospy.sleep(0.2)
        break


def func_gen_attenuated_center(time, amp, time_const, f):
    motor_vel = amp * exp(-time_const * time) * (f * cos(f * time) - sin(f * time))
    return motor_vel


def func_gen_attenuated_side(time, amp, time_const, f, phase_shift):
    motor_vel = -amp * exp(-time_const * time) * (
                time_const * sin(f * (time + phase_shift)) - f * cos(f * (time + phase_shift)) + time_const)
    return motor_vel


def func_gen_sine_phase_shift(time, amp, frq_const, T_frq):
    motor_vel = (amp / frq_const) * sin((2 * pi / (T_frq * frq_const)) * (time + (T_frq * frq_const) / 4))
    return motor_vel


def func_gen_validation(time, amp, time_const, f):
    motor_vel = 0
    return motor_vel


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
        talker()
    except:
        pass
