#!/usr/bin/env python3

######################################################

# This script is a fixed jacobian matrix and compute the desired angular value/velocity

# sub topic(std_msgs.msg/Float64): /p_error, /predicted_jacobian_value
# pub topic(rospy_tutorials.msg/Floats): /vel_array


######################################################

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats

p_error = 0.0
kp = 2.0
fixed_jacobian = 1
robot_movement_array = Floats()
robot_movement_array.data = [0.0, 0.0, 0.0, 0.0, 0.0]


def callback_p_error(msg):
    global p_error
    p_error = msg.data


def callback_kp(msg):
    global kp
    kp = msg.data


def P_controller():
    rospy.init_node('VS_fixed_Jacobian', anonymous=True)
    r = rospy.Rate(100.0)  # Hz
    rospy.Subscriber("/p_error", Float64, callback_p_error)
    rospy.Subscriber("/kp", Float64, callback_kp)
    pub = rospy.Publisher('/vel_array', Floats, queue_size=1)
    alpha = 1.0

    while not rospy.is_shutdown():
        desired_vel = p_error * (kp / fixed_jacobian)
        robot_movement_array.data = [desired_vel, 0.0, 0.0, 0.0, 0.0]
        # robot_movement_array.data = [0.0, 0.0, 0.0, desired_vel, 0.0]
        pub.publish(robot_movement_array)
        print(kp)
        r.sleep()

    return


if __name__ == '__main__':
    try:
        P_controller()
    except:
        pass
