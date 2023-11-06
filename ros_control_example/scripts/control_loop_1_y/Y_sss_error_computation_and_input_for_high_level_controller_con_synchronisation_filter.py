#!/usr/bin/env python
# coding: utf8
# to soòve the SyntaxError: Non-ASCII character '\xc3' in file

#here we create a sever collecting all data needed by the high level controller (desired input and sensors data)

#this time it is a standard way ro create a service 
#rospy.Service('/high_level_input_data_server', Floats_array, my_server)
#

import rospy
import message_filters
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector

t_sec = 0
t_nsec = 0
cam_x = 0
cam_y = 0 
pos_in_x = 0
pos_in_y = 0
error_x = 0
error_y = 0
q_1 = 0
q_2 = 0

def callback(camera_pos, desired_pos, joint_2):
  # The callback processing the pairs of numbers that arrived at approximately the same time
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,t_sec,t_nsec,q_1,q_2
    cam_x=camera_pos.data[0]
    cam_y=camera_pos.data[1]
    t_sec=camera_pos.data[3]
    t_nsec=camera_pos.data[4]    
    pos_in_x=desired_pos.data[0]
    pos_in_y=desired_pos.data[1]
    q_2=joint_2.data[0]
    error_x = pos_in_x-cam_x
    error_y = pos_in_y-cam_y    



def error_computation():
    global cam_x,cam_y,pos_in_x,pos_in_y,error_x,error_y,t_sec,t_nsec,q_1,q_2

    freq = 40

    rospy.init_node('data_collector_for_error_computation_sync')
    dp_sub = message_filters.Subscriber('detecting_point', Floats)
    dc_sub = message_filters.Subscriber('/desired_command', Floats)
    j2_sub = message_filters.Subscriber('/joint_states_from_arduino_2', Floats)

    ts = message_filters.ApproximateTimeSynchronizer([dp_sub, dc_sub, j2_sub], 1, 0.15, allow_headerless=True) # 100 è lo slope, massimo delta t tra i tempi di arrivo (in secondi) consentito per accoppiare 2 messaggi, setroppo stretto ed i messaggi dai 2 topic arrivano sempre ad un delta t maggiore di quello indicato non verrà mai sottoscritto nulla ed i valori pubblicati saranno sempre quelli di inizializzazione 0 0 0 0 0 0
#    ts = message_filters.ApproximateTimeSynchronizer([dp_sub, dc_sub, j1_sub, j2_sub], 1, 60, allow_headerless=True) credo non funzioni perchè sta aspettando che venga pubblicato qualcosa da /joint_states_from_arduino_2 ma qui non viene pubblicato nulla, quindi è tuttoo bloccato sebbene in rqt_graph è tutte le connessioni sono segnate correttamente quindi per ora inseriamo solo j1_sub 

    ts.registerCallback(callback)

    #pub = rospy.Publisher('/error_and_data_for_error_computation', Floats, queue_size=1)  linea di codce ufficiale
    pub = rospy.Publisher('/error_and_data_for_error_computation_test', Floats, queue_size=1)  #linea di codce di prova da sostoture con quella sopra quando si fanno le prove con il robot

    rate = rospy.Rate(freq) # hz

    while not rospy.is_shutdown():
	

	err_data = Floats()
	err_data.data = [pos_in_x,pos_in_y,cam_x,cam_y,error_x,error_y,q_1,q_2,t_sec,t_nsec]	
        rospy.loginfo(err_data)
        pub.publish(err_data)
	rate.sleep()
	
		
if __name__ == '__main__':
    try:
        error_computation()
    except rospy.ROSInterruptException:
        pass



#class message_filters.ApproximateTimeSynchronizer(fs, queue_size, slop, allow_headerless=False, reset=False)


#import message_filters
#from sensor_msgs.msg import Image, CameraInfo

#def callback(image, camera_info):
  # Solve all of perception here...

#image_sub = message_filters.Subscriber('image', Image)
#info_sub = message_filters.Subscriber('camera_info', CameraInfo)

#ts = message_filters.TimeSynchronizer([image_sub, info_sub], 10)
#ts.registerCallback(callback)
#rospy.spin()



#import message_filters
#from std_msgs.msg import Int32, Float32

#def callback(mode, penalty):
  # The callback processing the pairs of numbers that arrived at approximately the same time

#mode_sub = message_filters.Subscriber('mode', Int32)
#penalty_sub = message_filters.Subscriber('penalty', Float32)

#ts = message_filters.ApproximateTimeSynchronizer([mode_sub, penalty_sub], 10, 0.1, allow_headerless=True)
#ts.registerCallback(callback)
#rospy.spin()


