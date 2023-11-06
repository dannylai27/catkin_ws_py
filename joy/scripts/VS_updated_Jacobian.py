#!/usr/bin/env python3

######################################################

# This script is used to update jacobian and compute the desired angular value/velocity

# sub topic(std_msgs.msg/Float64): /p_error, /predicted_jacobian_value
# pub topic(rospy_tutorials.msg/Floats): /vel_array


######################################################

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats

global p_error
p_error = 0.0
initial_jacobian = 1
new_jacobian = initial_jacobian  # this should be the initialized jacobian value
robot_movement_array = Floats()
robot_movement_array.data = [0.0, 0.0, 0.0, 0.0, 0.0]


def callback_new_jacobian(msg):
    global new_jacobian
    new_jacobian = msg.data


def callback_p_error(msg):
    global p_error
    p_error = msg.data


def P_controller(kp=1):
    rospy.init_node('update_Jacobian', anonymous=True)
    r = rospy.Rate(100.0)  # Hz
    rospy.Subscriber("/predicted_jacobian_value", Float64, callback_new_jacobian)
    rospy.Subscriber("/p_error", Float64, callback_p_error)
    pub = rospy.Publisher('/vel_array_mock', Floats, queue_size=1)
    alpha = 0.3

    while not rospy.is_shutdown():
        updated_jacobian = (1.0 - alpha) * initial_jacobian + alpha * new_jacobian
        desired_vel = p_error * (1.0 / updated_jacobian)
        robot_movement_array.data = [desired_vel, 0.0, 0.0, 0.0, 0.0]
        pub.publish(robot_movement_array)
        r.sleep()

    return


if __name__ == '__main__':
    try:
        P_controller()
    except:
        pass
