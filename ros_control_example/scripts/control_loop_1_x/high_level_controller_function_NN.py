#!/usr/bin/env python

# DEFINE YOUR HIGH LEVEL CONTROLLER HERE

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector
###############################################################################################
#let's add what needed by the NN
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
import tensorflow as tf
import math
import pandas as pd
###################################################################################################

# pos_in, p_x, p_y, p_z, o_x, o_y, o_z, o_w, pos_m1, vel_m1, pos_m2, vel_m2, cam_x, cam_y


def controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1_old, q_2_old,new_model,data_buffer):


  	
    command = Floats()
    deg_to_rad = 3.14/180.0  #(rads/degree)
    calib_x = 0.21 #120.0/560.0  #90.0/550.0 old slope # slope from calibration of x (degrees / pixel)
    calib_y = 1
    p_controller_x = 0.8 # old p 0.5
     
#     command = Float64()

#### IMPLEMENT HERE THE CONTROLLER ##############################
     

    b = 17

    NN_input = np.zeros([1,5])
    NN_input[0][0] = data_buffer[0][2] + data_buffer[0][4] 
    NN_input[0][1] = data_buffer[1][2] + data_buffer[1][4] 
    NN_input[0][2] = data_buffer[2][2] + data_buffer[2][4] 
    NN_input[0][3] = data_buffer[3][2] + data_buffer[3][4] 
    NN_input[0][4] = data_buffer[4][2] + data_buffer[4][4] 
    y_predicted = new_model.predict(NN_input)
    

 #   for i in range(b):
#	    cam_x_official_arr_testing[0][0] = 15*i
#	    y_predicted = new_model.predict(cam_x_official_arr_testing)
#	    print("i alias cam x and y_predicted alias q_1 ")
#	    print(cam_x_official_arr_testing[0][0])
#	    print(y_predicted[0][0])
#	    print("------------------")    

############################################

#     command.data = [cam_x, pos_in_x] #a value

    #command.data = [p_controller_x * error_x * calib_x* deg_to_rad +q_1_old * deg_to_rad, 0] #a value
    command.data = [y_predicted, 0] #a value

############################################

    return command


