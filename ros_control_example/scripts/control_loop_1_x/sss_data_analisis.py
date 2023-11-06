#!/usr/bin/env python


#it will collect data from the server and publish on the command topic
# http://wiki.ros.org/rospy/Overview/Services

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector
import high_level_controller_function as high_controller

t_sec = 0
t_nsec = 0
t_sec_old = 0
t_nsec_old = 0
cam_x = 0
cam_y = 0 
pos_in_x = 0
pos_in_y = 0
error_x = 0
error_y = 0
q_1 = 0
q_2 = 0

def callback_error_and_data(variable_of_callback_error_and_data):
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,t_sec,t_nsec
    cam_x=variable_of_callback_error_and_data.data[0]
    cam_y=variable_of_callback_error_and_data.data[1]
    pos_in_x=variable_of_callback_error_and_data.data[2]
    pos_in_y=variable_of_callback_error_and_data.data[3]
    error_x=variable_of_callback_error_and_data.data[4]
    error_y=variable_of_callback_error_and_data.data[5]
    t_sec=variable_of_callback_error_and_data.data[6]
    t_nsec=variable_of_callback_error_and_data.data[7]

def q1_data(variable_of_callback_q1_data):
    global q_1
    q_1 = variable_of_callback_q1_data.data[0]

def q2_data(variable_of_callback_q2_data):
    global q_2
    q_2 = variable_of_callback_q2_data.data[0]

def high_control():
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,q_1,q_2,t_sec,t_nsec

    d = Floats()
    d.data =[cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,q_1,q_2,t_sec,t_nsec]

    freq = 40

    rospy.init_node('data_analizer')
    rospy.Subscriber("error_and_data_for_error_computation_test", Floats, callback_error_and_data, queue_size=1)
    rospy.Subscriber("/joint_states_from_arduino_1", Floats, q1_data, queue_size=1)
    rospy.Subscriber("/joint_states_from_arduino_2", Floats, q2_data, queue_size=1)


    pub = rospy.Publisher('/all_data', Floats, queue_size=1)  #desired_position_in_joints_space
    rate = rospy.Rate(freq) # hz

    while not rospy.is_shutdown():
	if (t_sec != t_sec_old or t_nsec != t_nsec_old):
		d.data =[cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,q_1,q_2,t_sec,t_nsec]
        rospy.loginfo(d)
        pub.publish(d)
	rate.sleep()
	
		
if __name__ == '__main__':
    try:
        high_control()
    except rospy.ROSInterruptException:
        pass

