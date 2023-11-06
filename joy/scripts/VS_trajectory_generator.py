#!/usr/bin/env python3

######################################################

### This script is used to generate trajectory in camera space!

# sub topic: None
# pub topic(std_msgs.msg/Float64): /desired_trajectory_CV, /kp
#     topic


######################################################

import rospy
from std_msgs.msg import Float64
from math import cos, sin, pi, exp
from scipy import signal
import numpy as np


def trajectory_gen():
    rospy.init_node('desired_trajectory_CV', anonymous=True)
    r = rospy.Rate(100)  # Hz
    set_point = Float64()
    kp = Float64()
    set_point.data = 0.0
    # amp = 1000.0  # 400/500/600/800
    # T_frq = 4.0  # 8/10/12/16
    # frq_const = 1  # this is used to change the period for experiments
    # # f = 1 / (T_frq * frq_const)
    # f = 2 * pi / (T_frq * frq_const)
    # phase_shift = 6 * T_frq * frq_const / 8
    # time_const = 0.2
    # # T_frq * frq_const is the real Period!
    pub = rospy.Publisher('/desired_trajectory_CV', Float64, queue_size=1)
    pub2 = rospy.Publisher('/kp', Float64, queue_size=1)
    init_time = rospy.get_time()
    t_period = 6.0  #6.0/4.0
    previous_flag = 0.0
    occurrences = 1.0
    k = 3.0
    time_current = 0.0
    rospy.sleep(0.5)
    while not (rospy.is_shutdown() or time_current > t_period*4.0*4.0):  # t_period*12.0*8.0
        now = rospy.get_time()
        time_current = now - init_time
        flag = signal.square(time_current*(2.0*pi)/t_period)
        if flag > 0:
            cv_x, _ = camera_space_transform(40.0+(occurrences*3.0), 0.0)
        else:
            cv_x, _ = camera_space_transform(-40.0-(occurrences*3.0), 0.0)

        if (np.sign(previous_flag) == -1.0 and np.sign(flag) == 0.0) or \
                (np.sign(previous_flag) == -1.0 and np.sign(flag) == 1.0):
            print(occurrences, k)
            occurrences = occurrences + 1.0
            if occurrences == 5.0:
                k = k + 0.5
                occurrences = 1.0
                if k == 5.0:
                    k = 3.0

        previous_flag = flag
        set_point.data = cv_x
        pub.publish(set_point)
        kp.data = k
        pub2.publish(kp)
        # rospy.loginfo(rospy.get_caller_id() + "  setpoint value: %s; time: %.3f; flag:%s",
        #               set_point.data,
        #               time_current,
        #               flag
        #               )
        r.sleep()

    return

def camera_space_transform(x, y):

    x = x + 125
    y = -y + 125

    return x, y


def func_gen(ros_time, freq, amp, function="cos"):
    if function == "cos":
        y = amp * cos(2 * pi * ros_time / freq)
    elif function == "sin":
        y = amp * sin(2 * pi * ros_time / freq)
    else:
        y = 0

    return y


if __name__ == '__main__':
    try:
        trajectory_gen()
    except:
        pass
