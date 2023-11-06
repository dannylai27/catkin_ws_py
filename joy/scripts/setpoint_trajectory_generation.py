#!/usr/bin/env python3

######################################################

### This script is used to generate trajectory for ros pid package!

######################################################
# sub topic:
# pub topic:


# required library
import rospy
from math import cos, sin, pi, exp
# required message types
from sensor_msgs.msg import Joy
from rospy_tutorials.msg import Floats
from std_msgs.msg import Float64

# global variable:
global set_point
set_point = Float64()
set_point.data = 0.0


def talker():
    rospy.init_node('auto_pub', anonymous=True)
    r = rospy.Rate(100)  # Hz
    amp = 1600.0  # 400/500/600/800
    T_frq = 4.0  # 8/10/12/16
    frq_const = 1  # this is used to change the period for experiments
    # f = 1 / (T_frq * frq_const)
    f = 2 * pi / (T_frq * frq_const)
    phase_shift = 6 * T_frq * frq_const / 8
    time_const = 0.2
    # T_frq * frq_const is the real Period!
    pub_M3 = rospy.Publisher('/setpoint_M3', Float64, queue_size=10)
    pub_M4 = rospy.Publisher('/setpoint_M4', Float64, queue_size=10)
    rospy.sleep(0.2)
    init_time = rospy.get_time()
    while not rospy.is_shutdown():
        now = init_time
        ros_time = now - init_time
        while ros_time < 2 * T_frq * frq_const:
            ros_time = now - init_time
            # set_point.data = amp*exp(-time_const*ros_time)*(f*cos(f*ros_time)-sin(f*ros_time))
            # set_point.data = (amp / frq_const) * sin(
            #     (2 * pi / (T_frq * frq_const)) * (ros_time + (T_frq * frq_const) / 4))
            # set_point.data = -amp * exp(-time_const * ros_time) * (
            #         time_const * sin(f * (ros_time + phase_shift)) - f * cos(
            #                 f * (ros_time + phase_shift)) + time_const)
            temp = amp * sin(2*pi*ros_time/(T_frq*frq_const))
            #######
            # if temp > 0:
            #     set_point.data = amp
            # elif temp < 0:
            #     set_point.data = -amp
            # else:
            #     set_point.data = 0.0
            #######
            set_point.data = temp
            #######
            pub_M3.publish(set_point)
            pub_M4.publish(set_point)
            rospy.loginfo(rospy.get_caller_id() + "  setpoint value: %s;  rostime: %s ",
                          set_point.data,
                          ros_time)
            r.sleep()
            now = rospy.get_time()

        set_point.data = 0.0
        pub_M3.publish(set_point)
        pub_M4.publish(set_point)
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
        talker()
    except:
        pass
