#!/usr/bin/env python

# DEFINE YOUR HIGH LEVEL CONTROLLER HERE

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector
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

# pos_in, p_x, p_y, p_z, o_x, o_y, o_z, o_w, pos_m1, vel_m1, pos_m2, vel_m2, cam_x, cam_y


def controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1_old, q_2_old, new_model, data_buffer_x_NN, data_buffer_y_NN, na, nb, L):


  	
    command = Floats()
    deg_to_rad = 3.14/180.0  #(rads/degree)
    calib_x = 0.21 #120.0/560.0  #90.0/550.0 old slope # slope from calibration of x (degrees / pixel)
    calib_y = -0.36 #50/-140 (degrees / pixel)
    p_controller_x = 0.8 # old p 0.5
    p_controller_y = 0.8 # old p 0.5
    b_predicted = 0.21
    b_predicted_temp = 0.20 
    calib_y_max = 0.5
    calib_y_min = -0.5

#################### MA FILTER ################################## ---------------------------
# to delete the filter, just comment the line below
#    cam_y = ( data_buffer_y_NN[0][0] + data_buffer_y_NN[1][0] + data_buffer_y_NN[2][0] ) / 3.0


#### IMPLEMENT HERE THE CONTROLLER ############################## ----------------------------
     

    forecast_data_array = np.zeros(L+1) # predictions with the new modality to be compared with y_predicted and real data 

    # REMEMBER THAT
    # line index of forecast_data_array contains [[q*_k q*_k+1 q*_k+2... q*_k+l]]
    # [q*_index q*_index+1 q*_index+2 ... q*_index+6] since l = 6  

    temp_array = np.zeros([1,nb+na+2])  

    y_future = np.zeros(L+1)
 
# x_future = [X_t X_t+1... X_t+L], L = 10 so x_future = [X_t X_t+1... X_t+10]
# We set X_t = cam_x, 
# X_t+w = cam_x + (pos_in_x - cam_x)*(1/L) * w
# In general
# X_t+L = cam_x + (pos_in_x - cam_x)*(1/L) * L = pos_in_x

#    print("-----inzio ciclo------")

    forecast_data_array[0] = data_buffer_y_NN[0][4]

    for w in range(L+1):
      y_future[w] = cam_y+(pos_in_y-cam_y)/L*w
#      print("x_future")
#      print(x_future[w]) #x_future[w]


    for z in range(L):
      if(z==0):
          for r in range(na+nb+2):
            temp_array[0][r] = data_buffer_y_NN[0][r]
#            print("temp_array iniziale:")
#            print(temp_array[0][r])
#            print("-")
          for s in range(nb):
            temp_array[0][nb-s] = temp_array[0][nb-s-1] # updating x

  	  temp_array[0][0] = y_future[z+1]
#          print("Tempo 1:")
#          t = rospy.Time.now()
#	  print(t.secs)
#	  print(t.nsecs)
          q_forecast = new_model.predict(temp_array)
#          print("Tempo 2:")
#          t = rospy.Time.now()
#	  print(t.secs)
#	  print(t.nsecs)
          forecast_data_array[z+1] = q_forecast
      else:
          for v in range(na-1):
            temp_array[0][nb+na-v] = temp_array[0][nb+na-v-1] # updating q
#            print("temp_array q:")
#            print(nb+na-v)
#            print("---")
#            print(temp_array[0][nb+na-v])

          temp_array[0][nb+1] = q_forecast
#          print("q_forecast q or temp_array[3] new:") 
#          print(q_forecast)   
 
          for s in range(nb):
            temp_array[0][nb-s] = temp_array[0][nb-s-1] # updating x
#            print("temp_array cam:")
#            print(nb-s)
#            print("---")
#            print(temp_array[0][nb-s])
          
          temp_array[0][0] = y_future[z+1]
          q_forecast = new_model.predict(temp_array)
          forecast_data_array[z+1] = q_forecast
    
############################################-----------------------------------
    sum_y = 0.0
    sum_y2 = 0.0
    sum_q2 = 0.0
    sum_yq2 = 0.0
    N = L+1

    for i in range(N):
    	sum_y = sum_y + y_future[i]
	sum_y2 = sum_y2 + y_future[i] * y_future[i]
	sum_q2 = sum_q2 +  forecast_data_array[i]
	sum_yq2 = sum_yq2 + y_future[i] * forecast_data_array[i]
#        print("forecast_data_array")
#        print(forecast_data_array[i])

# Regression line y = a + b * x in this case q1 = a + b * x obtained reducing the mean squared error

# a_predicted = ( sum_y_predicted * sum_x2 - sum_x * sum_xy_predicted ) / ( n * sum_x2 - sum_x * sum_x )
	
    if (( N * sum_y2 - sum_y * sum_y )!= 0): # to avoid the condition num/0 = not a number
    	b_predicted_temp = ( N * sum_yq2 - sum_y * sum_q2 ) / ( N * sum_y2 - sum_y * sum_y )
	if ( b_predicted_temp < calib_y_max or b_predicted_temp > calib_y_min ): #to avoid a slope of infinite module
		b_predicted = b_predicted_temp    
		
    calib_y = b_predicted

    print("calib_y:")
    print(calib_y)
    print("b_predicted_temp:")
    print(b_predicted_temp)
    print("b_predicted:")
    print(b_predicted)
    print(" N * sum_y2 - sum_y * sum_y:")
    print(N * sum_y2 - sum_y * sum_y)
    print("y_future:")
    print(y_future[0])
    print(y_future[1])
    print(y_future[2])
    print(y_future[3])
#    print(y_future[4])
#    print(y_future[5])
    print("forecast_data_array:")
    print(forecast_data_array[0])
    print(forecast_data_array[1])
    print(forecast_data_array[2])
    print(forecast_data_array[3])
#    print(forecast_data_array[4])
#    print(forecast_data_array[5])
    print("data_buffer_x_NN[i][0]:")
    print(data_buffer_y_NN[0][0])
    print(data_buffer_y_NN[1][0])
    print(data_buffer_y_NN[2][0])
    print(data_buffer_y_NN[3][0])

# in the python script I use eror_x = x_future[1] - x_future[0]

    #T = x_future[1] # cam_x+(pos_in_x-cam_x)/L*2
#    print("calib_x")
#    print(calib_x)
#    print("-")
#    print(N * sum_x2 - sum_x * sum_x)
#    print("-----fine ciclo------")
############################################------------------------------------

# NN controller for x (motor 1), position fixed for y (motor 2)

    command.data = [ 0 , p_controller_y * error_y * calib_y * deg_to_rad + q_2_old * deg_to_rad ] 

# NN controller for x, P controller for y
# command.data = [ p_controller_x * error_x * calib_x* deg_to_rad +q_1_old * deg_to_rad , p_controller_y * error_y * calib_y * deg_to_rad + q_2_old * deg_to_rad]

############################################

    return command


