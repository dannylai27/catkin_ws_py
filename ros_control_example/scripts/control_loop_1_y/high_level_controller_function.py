#!/usr/bin/env python

# DEFINE YOUR HIGH LEVEL CONTROLLER HERE

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector


# pos_in, p_x, p_y, p_z, o_x, o_y, o_z, o_w, pos_m1, vel_m1, pos_m2, vel_m2, cam_x, cam_y


def controller(pos_in_x, pos_in_y, cam_x, cam_y, error_x, error_y, q_1_old, q_2_old):


  	
    command = Floats()
    deg_to_rad = 3.14/180.0  #(rads/degree)
    calib_x = 0.21 #120.0/560.0  #90.0/550.0 old slope # slope from calibration of x (degrees / pixel)
    calib_y = 1
    p_controller_x = 0.8 # old p 0.5
     
#     command = Float64()

#### IMPLEMENT HERE THE CONTROLLER ##############################
     
#     POS_IN = pos_in
#     P_X = p_x
#     P_Y = p_y
#     P_Z = p_z
#     O_X = o_x
#     O_Y = o_y
#     O_Z = o_z
#     O_W = o_w
#     POS_M1 = pos_m1
#     VEL_M1 = vel_m1
#     POS_M2 = pos_m2
#     VEL_M2 = vel_m2
#     CAM_X = cam_x
#     CAM_Y = cam_y
     
     #command.data = "0.7"
#     command.data = 


############################################

#     command.data = [cam_x, pos_in_x] #a value

    command.data = [p_controller_x * error_x * calib_x* deg_to_rad +q_1_old * deg_to_rad, 0] #a value

############################################

    return command


