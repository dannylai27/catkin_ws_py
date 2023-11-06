#!/usr/bin/env python3
"""
#######################################################################################################################

# This script is used to send position to PID package to control (Arduino Driver)Flexy_2_stepper_PID_DUE_drivers.io!

#######################################################################################################################
"""

import rospy
from math import cos, sin, pi, exp
from std_msgs.msg import Float64


class FlexyRobotEncoders:
    def __init__(self):
        self.M1 = Float64()
        self.M2 = Float64()
        self.M3 = Float64()
        self.M4 = Float64()
        self.M1.data = 0.0
        self.M2.data = 0.0
        self.M3.data = 0.0
        self.M4.data = 0.0


def auto_set_pos_publisher():
    rospy.init_node('auto_set_pos_publisher', anonymous=True)
    r = rospy.Rate(60)  # TODO: Find the proper rate in previous scripts
    pub_M1 = rospy.Publisher('/setpoint_M1', Float64, queue_size=0)
    pub_M2 = rospy.Publisher('/setpoint_M2', Float64, queue_size=0)

    rospy.sleep(1)  # sleep to wait other nodes initializing
    init_time = rospy.get_time()  # init_time is used to calculate the f(t)
    Encoders = FlexyRobotEncoders()
    while not rospy.is_shutdown():
        now = rospy.get_time()  # starts of a new loop
        ros_time = now - init_time  # 'ros_time' is the time in f(t)
        Encoders.M1.data = func_gen(ros_time, amp=100, period=10)
        pub_M1.publish(Encoders.M1)
        pub_M2.publish(Encoders.M2)
        r.sleep()


def func_gen(ros_time, period=1, amp=1, function="sin"):
    if function == "cos":
        y = amp * cos(2 * pi * ros_time / period)
    elif function == "sin":
        y = amp * sin(2 * pi * ros_time / period)
    else:
        y = 0

    return y


if __name__ == '__main__':
    try:
        auto_set_pos_publisher()
    except:
        pass
