#!/usr/bin/env python


import rospy
from std_msgs.msg import Float64




def wave():

    amplitude = Float64()
    freq = 40  # Hz
    sample = 0
    total_ite = 0
    init = True	
    pub = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)
    rospy.init_node('square_wave_generator', anonymous=True)
    rate = rospy.Rate(freq) # hz
    cycle_test = 50
    while not rospy.is_shutdown():
	if init is True:
		amplitude.data = 0.0
	        rospy.loginfo(amplitude)
        	pub.publish(amplitude)
        	rate.sleep()
		init = False
	else: 	
        	if sample <= 400 and total_ite < cycle_test:
			amplitude.data = 0.7
	        	rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
		elif sample > 400 and total_ite < cycle_test:
			amplitude.data = -0.7
			rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
                elif total_ite > cycle_test:
                        amplitude.data = 0.0
                        rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()

		sample +=1
		if sample == 800 :
                        total_ite +=1 
			sample = 0	#sample variable might be useful in case of sine function
						
		
		
if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass

