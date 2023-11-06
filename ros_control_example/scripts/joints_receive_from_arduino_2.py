#!/usr/bin/env python
import rospy
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
pos=0
vel=0

def my_callback(msg):
    global pos, vel
    pos=msg.data[0]
    vel=msg.data[1]
    #print "Pos: ", pos, "vel: ", vel

def my_server(req):
    global pos, vel
    res = Floats_arrayResponse() 
    res.res=[pos, vel]
    return res

rospy.init_node('subscriber_2_py') #initialzing the node with name "subscriber_py"

rospy.Subscriber("/joint_states_from_arduino_2", Floats, my_callback, queue_size=2) 

rospy.Service('/read_joint_state_2', Floats_array, my_server)

rospy.spin() 
