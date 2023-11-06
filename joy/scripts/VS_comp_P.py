#!/usr/bin/env python3

######################################################

### This script is compare the error from desired_trajectory_CV and actual_target_pos

# sub topic(std_msgs.msg/Float64): desired_trajectory_CV
#          (target_centroid/Floats):target_centroid
# pub topic(std_msgs.msg/Float64): P_error


######################################################

import rospy
from std_msgs.msg import Float64
from target_centroid import Floats


# global desired_trajectory_CV, actual_target_pos_CV
actual_target_pos_CV = 125.0
desired_trajectory_CV = 125.0

def callback_desired_trajectory(data):
    global desired_trajectory_CV
    desired_trajectory_CV = data.data


def callback_actual_target(data):
    global actual_target_pos_CV
    actual_target_pos_CV = data.data[0]


def P_controller(kp=1):
    rospy.init_node('desired_trajectory_CV', anonymous=True)
    r = rospy.Rate(100)  # Hz
    p_error = Float64()
    p_error.data = 0.0
    rospy.Subscriber("/desired_trajectory_CV", Float64, callback_desired_trajectory)
    rospy.Subscriber("/target_centroid", Floats, callback_actual_target)
    pub = rospy.Publisher('/p_error', Float64, queue_size=1)
    while not rospy.is_shutdown():
        p_error.data = kp * (desired_trajectory_CV - actual_target_pos_CV)
        pub.publish(p_error)
        rospy.loginfo(rospy.get_caller_id() + "  p_error value is : %s  ",
                      p_error.data,
                      )
        r.sleep()

    return


if __name__ == '__main__':
    try:
        P_controller()
    except:
        pass
