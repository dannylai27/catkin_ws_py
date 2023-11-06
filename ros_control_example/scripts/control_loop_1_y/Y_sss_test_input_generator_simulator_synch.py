#!/usr/bin/env python


#it will collect data from the server and publish on the command topic

import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from ros_control_example.srv import Floats_array, Floats_arrayResponse, Floats_arrayRequest
from ndi_aurora_msgs.msg import AuroraData, AuroraDataVector



def wave():
    flag = True
#    i = 0
    amplitude =  Floats()
    pub = rospy.Publisher('/desired_command', Floats, queue_size=1)
    rospy.init_node('desired_position_generator', anonymous=True)
    rate = rospy.Rate(40) # hz 
 
    while not rospy.is_shutdown():
#                t = rospy.Time.now()
		if flag == True:
			amplitude.data = [320, 240] # half width/height of the image size
	        	rospy.loginfo(amplitude)
        		pub.publish(amplitude)
                        flag = False
        		rate.sleep()
		else:
			amplitude.data = [320, 240]
	        	rospy.loginfo(amplitude)
        		pub.publish(amplitude)
                        flag = True
        		rate.sleep() 

	
		




if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass

#rostopic pub /test_aurora ndi_aurora_msgs/AuroraData "position: {x: 0.0, y: 0.0, z: 0.0}
#orientation: {x: 0.0, y: 0.0, z: 0.0, w: 0.0}
#error: 0.0
#visible: false
#portHandle: 0"



#    while not rospy.is_shutdown():
#                t = rospy.Time.now()
#		if flag == True:
#                	i = i+1
#			amplitude.data = [t.secs, t.nsecs]
#	        	rospy.loginfo(amplitude)
#        		pub.publish(amplitude)
#                        flag = False
#        		rate.sleep()
#		else:
#                	i = i+1
#			amplitude.data = [-t.secs, -t.nsecs]
#	        	rospy.loginfo(amplitude)
#        		pub.publish(amplitude)
#                        flag = True
#        		rate.sleep() 
