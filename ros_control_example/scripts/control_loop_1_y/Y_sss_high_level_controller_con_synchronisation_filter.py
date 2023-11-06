#!/usr/bin/env python


#it will collect data from the server and publish on the command topic
# http://wiki.ros.org/rospy/Overview/Services

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector
# import high_level_controller_function as high_controller  #to use the basic P controller
import high_level_controller_function_NN as high_controller #to use the NN controller


###############################################################################################
#let's add what needed by the NN
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf
import math
import pandas as pd
###################################################################################################

t_sec = 0
t_nsec = 0
t_sec_old = 0
t_nsec_old = 0
cam_x = 0
cam_y = 0 
pos_in_x = 320 # desired target x in image plane
pos_in_y = 240 # desired target y
error_x = 0
error_y = 0
q_1 = 0
q_2 = 0
pid_input_1 = Float64()
pid_input_2 = Float64()
pid_input = Float64()
pid_input.data = [0.0 , 0.0]

def callback_error_and_data(variable_of_callback_error_and_data):
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,t_sec,t_nsec,q_1,q_2
    cam_x=variable_of_callback_error_and_data.data[0]
    cam_y=variable_of_callback_error_and_data.data[1]
    pos_in_x=variable_of_callback_error_and_data.data[2]
    pos_in_y=variable_of_callback_error_and_data.data[3]
    error_x=variable_of_callback_error_and_data.data[4]
    error_y=variable_of_callback_error_and_data.data[5]
    q_1=variable_of_callback_error_and_data.data[6]
    q_2=variable_of_callback_error_and_data.data[7]
    t_sec=variable_of_callback_error_and_data.data[8]
    t_nsec=variable_of_callback_error_and_data.data[9]

#def callback_joint_1(variable_of_callback_joint_1):
#    global q_1
#    q_1=variable_of_callback_joint_1.data[0]

#def callback_joint_2(variable_of_callback_joint_2):
#    global q_2
#    q_2=variable_of_callback_joint_2.data[0]


def high_control():
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,t_sec,t_nsec,pid_input,q_1,q_2

    freq = 40

    rospy.init_node('high_level_controller_synch')
    rospy.Subscriber("error_and_data_for_error_computation_test", Floats, callback_error_and_data, queue_size=1)
#    rospy.Subscriber("/joint_states_from_arduino_1", Floats, callback_joint_1, queue_size=1)
#    rospy.Subscriber("/joint_states_from_arduino_2", Floats, callback_joint_2, queue_size=1)

    pub1 = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)  #desired_position_in_joints_space
    pub2 = rospy.Publisher('/single_joint_actuator/joint2_position_controller/command', Float64, queue_size=1)  #desired_position_in_joints_space
    rate = rospy.Rate(freq) # hz
 
###############################################################################################
#let's add what needed by the NN, we do not do it in the function otherwise these commands will be repeated at every call

    cam_x_official_to_validate = np.zeros([10,5]) # 5 buffer size dell' input della network
    q_1_official_to_validate = np.zeros([10,1])  #numero di input, di vettori di 5 elementi ciascuno che daremo in ingresso per la validazione


    new_model = tf.keras.models.load_model('/home/lorenzo/Scrivania/catkin_ws_soft_robot_light/zz_python_data_analisis/trained_models/my_model_with_buffer_good') 

    new_model.evaluate(cam_x_official_to_validate, q_1_official_to_validate)

    # Display the model
    new_model.summary()
###############################################################################################
# buffer
    k = 8
    d = 10 # buffer dimention
    data_buffer = np.zeros([d,k]) #k = 8 because pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1, q_2 are 8 values
###############################################################################################
    
    while not rospy.is_shutdown():
	if (True):#t_sec != t_sec_old or t_nsec != t_nsec_old
		for i in range(d):
			for j in range(k):
				if(i+1<d):	
					data_buffer[i+1][j] = data_buffer[i][j]
			if(i==0):
				data_buffer[i][0] = pos_in_x
				data_buffer[i][1] = pos_in_y
				data_buffer[i][2] = cam_x
				data_buffer[i][3] = cam_y
				data_buffer[i][4] = error_x
				data_buffer[i][5] = error_y
				data_buffer[i][6] = q_1
				data_buffer[i][7] = q_2
		 
		pid_input = high_controller.controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1, q_2,new_model,data_buffer)
	pid_input_1.data = pid_input.data[0]
	pid_input_2.data = pid_input.data[1]
        rospy.loginfo(pid_input_1)
        pub1.publish(pid_input_1)
        rospy.loginfo(pid_input_2)
        pub2.publish(pid_input_2)
	rate.sleep()
	
		
if __name__ == '__main__':
    try:
        high_control()
    except rospy.ROSInterruptException:
        pass


#!/usr/bin/env python


#it will collect data from the server and publish on the command topic
# http://wiki.ros.org/rospy/Overview/Services
#
#import rospy
#from std_msgs.msg import Float64
#from rospy_tutorials.msg import Floats
#from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
#from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector
#import high_level_controller_function as high_controller
#
#
#cam_x = 0
#cam_y = 0 
#pos_in_x = 0
#pos_in_y = 0
#error_x = 0
#error_y = 0
#pid_input = Float64()
#
#def callback_error_and_data(variable_of_callback_error_and_data):
#    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y
#    cam_x=variable_of_callback_error_and_data.data[0]
#    cam_y=variable_of_callback_error_and_data.data[1]
#    pos_in_x=variable_of_callback_error_and_data.data[2]
#    pos_in_y=variable_of_callback_error_and_data.data[3]
#    error_x=variable_of_callback_error_and_data.data[4]
#    error_y=variable_of_callback_error_and_data.data[5]
#
#
#def high_control():
#    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y
#
#    freq = 4
#
#    rospy.init_node('high_level_controller')
#    rospy.Subscriber("error_and_data_for_error_computation", Floats, callback_error_and_data, queue_size=1)
#
#    pub = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)  #desired_position_in_joints_space
#    rate = rospy.Rate(freq) # hz
#
#    while not rospy.is_shutdown():
#
#	pid_input = high_controller.controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y)
#        rospy.loginfo(pid_input)
#        pub.publish(pid_input)
#	rate.sleep()
#	
#		
#if __name__ == '__main__':
#    try:
#        high_control()
#    except rospy.ROSInterruptException:
#        pass
#
