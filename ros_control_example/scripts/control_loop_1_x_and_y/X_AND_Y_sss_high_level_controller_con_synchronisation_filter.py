#!/usr/bin/env python


#it will collect data from the server and publish on the command topic
# http://wiki.ros.org/rospy/Overview/Services

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector
import high_level_controller_function_P as high_controller_p  #to use the basic P controller (number 0)
import high_level_controller_function_NN_X as high_controller_nn_x #to use the NN controller on X (number 1)
import high_level_controller_function_NN_Y as high_controller_nn_y #to use the NN controller on Y (number 2)
#import high_level_controller_function_NN_X_and_Y_indipendent as high_controller_nn_x_and_y_indipendent #to use the NN controller on X and Y with 2 indipendent networks (number 3)
#import high_level_controller_function_NN_X_and_Y_dipendent as high_controller_nn_x_and_y_dipendent #to use the NN controller on X and Y with 1 network (number 4)
import time

###############################################################################################
#let's add what needed by the NN
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf
import math
import pandas as pd
###################################################################################################

# global variable declaration

t_sec = 0
t_nsec = 0
t_sec_old = 0
t_nsec_old = 0
cam_x = 320
cam_y = 240 
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
choose_type = 1  
# set the default high level controller (0 --> P_controller both for x and y)
# set the NN high level controller for X (1 --> NN_controller for x and P controller for y)
# set the NN high level controller for Y (2 --> NN_controller for y and P controller for x)
# set the NN high level controller for X and Y (3 --> NN_controller for x and NN controller for y, 2 indipendent networks)
# set the NN high level controller for X and Y (4 --> NN_controller for x and NN controller for x, 1 network working for both directions)

def callback_error_and_data(variable_of_callback_error_and_data):
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,t_sec,t_nsec,q_1,q_2
    pos_in_x=variable_of_callback_error_and_data.data[0]
    pos_in_y=variable_of_callback_error_and_data.data[1]
    cam_x=variable_of_callback_error_and_data.data[2]
    cam_y=variable_of_callback_error_and_data.data[3]
    error_x=variable_of_callback_error_and_data.data[4]
    error_y=variable_of_callback_error_and_data.data[5]
    q_1=variable_of_callback_error_and_data.data[6]
    q_2=variable_of_callback_error_and_data.data[7]
    t_sec=variable_of_callback_error_and_data.data[8]
    t_nsec=variable_of_callback_error_and_data.data[9]



def high_control():
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,t_sec,t_nsec,t_sec_old,t_nsec_old,pid_input,q_1,q_2,choose_type
    
    #	our network accepts as input a vector [x_t x_t-1... x_t-nb q_t-1 q_t-2... q(t-na) 1]
    #	and gives as output q*_t = F([x_t x_t-1... x_t-nb q_t-1 q_t-2... q(t-na) 1]) 
    #	where 
    #	x is the position in the image expressed in number of pixel
    #	q is the angle at motor level, in degrees
    #	t current time	

    na = 3	# network parameter
    nb = 2	# network parameter
    L = 3
    k = na+nb+2 # since [x(t) x(t-1)... x(t-nb) q(t-1) q(t-2)... q(t-na) 1]
    freq = 40 # frequency with which high_level_controller_synch will publish

    input_official_to_validate_q1_x_NN = np.zeros([10,na+nb+2])
    output_official_to_validate_q1_x_NN = np.zeros([10,1])

    input_official_to_validate_q2_y_NN = np.zeros([10,na+nb+2])
    output_official_to_validate_q2_y_NN = np.zeros([10,1])

    if na>nb:
	d = na+1	#d buffer length  
    else:
	d = nb+1

    data_buffer_x_NN = np.zeros([d,k])	# in case we will desire to realize a PID
    data_buffer_y_NN = np.zeros([d,k])

    rospy.init_node('high_level_controller_synch')
    rospy.Subscriber("error_and_data_for_error_computation_test", Floats, callback_error_and_data, queue_size=1)

    pub1 = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)  #desired_position_in_joints_space in radians
    pub2 = rospy.Publisher('/single_joint_actuator/joint2_position_controller/command', Float64, queue_size=1)  #desired_position_in_joints_space in radians
    rate = rospy.Rate(freq) # hz
 
#################################################################################################


    for i in range(10):
	for j1 in range(nb+1):
		input_official_to_validate_q1_x_NN[i][j1] = pos_in_x	
	for j2 in range(na):
		input_official_to_validate_q1_x_NN[i][nb+1+j2] = q_1	
	input_official_to_validate_q1_x_NN[i][nb+na+1] = 1
	output_official_to_validate_q1_x_NN[i] = q_1
	
    for i in range(10):
	for j1 in range(nb+1):
		input_official_to_validate_q2_y_NN[i][j1] = pos_in_y	
	for j2 in range(na):
		input_official_to_validate_q2_y_NN[i][nb+1+j2] = q_2	
	input_official_to_validate_q2_y_NN[i][nb+na+1] = 1
	output_official_to_validate_q2_y_NN[i] = q_2


# matrix of 10 rows where each row is
# [x(t) x(t-1)... x(t-nb) q(t-1) q(t-2)... q(t-na) 1]
# We fill everything with x = pos_in_x and q with q_1

    model_x = tf.keras.models.load_model('/home/lorenzo/Scrivania/catkin_ws_soft_robot_light/zz_python_data_analisis/trained_models/model_22_02_16_a3_and_a2') 

    model_x.evaluate(input_official_to_validate_q1_x_NN, output_official_to_validate_q1_x_NN)

    model_y = tf.keras.models.load_model('/home/lorenzo/Scrivania/catkin_ws_soft_robot_light/zz_python_data_analisis/trained_models/model_22_02_16_a3_and_a2_y_direction') 

    model_y.evaluate(input_official_to_validate_q2_y_NN, output_official_to_validate_q2_y_NN)

    for i in range(d):
	for j1 in range(nb+1):
		data_buffer_x_NN[i][j1] = pos_in_x	
	for j2 in range(na):
		data_buffer_x_NN[i][nb+1+j2] = q_1	
	data_buffer_x_NN[i][nb+na+1] = 1


    for i in range(d):
	for j1 in range(nb+1):
		data_buffer_y_NN[i][j1] = pos_in_y	
	for j2 in range(na):
		data_buffer_y_NN[i][nb+1+j2] = q_2	
	data_buffer_y_NN[i][nb+na+1] = 1

###############################################################################################
    
    while not rospy.is_shutdown():

	if (t_sec != t_sec_old or t_nsec != t_nsec_old): # I update the buffer only when new data arrives otherwise we would fill the buffer with the same values
 
		for i in range(d):
			if(i==d-1):
      				for v in range(na-1):
        				data_buffer_x_NN[d-1-i][nb+na-v] = data_buffer_x_NN[d-1-i][nb+na-v-1] # updating q
      				for s in range(nb):
          				data_buffer_x_NN[d-1-i][nb-s] = data_buffer_x_NN[d-1-i][nb-s-1] # updating x

				data_buffer_x_NN[d-1-i][0] = cam_x
				data_buffer_x_NN[d-1-i][nb+1] = q_1
			else:
				for j1 in range(k-1):
					data_buffer_x_NN[d-1-i][j1] = data_buffer_x_NN[d-1-i-1][j1]

		for i in range(d):
			if(i==d-1):
      				for v in range(na-1):
        				data_buffer_y_NN[d-1-i][nb+na-v] = data_buffer_y_NN[d-1-i][nb+na-v-1] # updating q
      				for s in range(nb):
          				data_buffer_y_NN[d-1-i][nb-s] = data_buffer_y_NN[d-1-i][nb-s-1] # updating x

				data_buffer_y_NN[d-1-i][0] = cam_y
				data_buffer_y_NN[d-1-i][nb+1] = q_2
			else:
				for j1 in range(k-1):
					data_buffer_y_NN[d-1-i][j1] = data_buffer_y_NN[d-1-i-1][j1]

	t_sec_old = t_sec
	t_nsec_old = t_nsec

	if (choose_type == 0):
		pid_input = high_controller_p.controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1, q_2, data_buffer_x_NN, data_buffer_y_NN) # P conntroller

	if (choose_type == 1):
                t1 = rospy.Time.now()
		pid_input = high_controller_nn_x.controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1, q_2, model_x, data_buffer_x_NN, data_buffer_y_NN, na, nb, L) 
                t2 = rospy.Time.now()
		print("tempo per eseguire la funzione con la NN:")
	        print(t2.secs - t1.secs)
	        print(t2.nsecs - t1.nsecs)

	if (choose_type == 2):
                t1 = rospy.Time.now()
		pid_input = high_controller_nn_y.controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1, q_2, model_y, data_buffer_x_NN, data_buffer_y_NN, na, nb, L) 
                t2 = rospy.Time.now()
		print("tempo per eseguire la funzione con la NN:")
	        print(t2.secs - t1.secs)
	        print(t2.nsecs - t1.nsecs)

# Not implemented yet
#	if (choose_type == 3):
#		pid_input = high_controller_nn_x_and_y_indipendent.controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1, q_2, data_buffer) # P conntroller

#	if (choose_type == 4):
#		pid_input = high_controller_nn_x_and_y_dipendent.controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1, q_2, data_buffer) # P conntroller
		

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

