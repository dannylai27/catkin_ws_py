#!/usr/bin/env python


import rospy
from std_msgs.msg import Float64




def wave():

    amplitude = Float64()
    freq = 40  # Hz sampling frequency
    a = 0.5 # amplitude square wave
    half_period = 10 # in seconds, frequency of the square wave (2*half_period)^(-1)
    h = freq*half_period
    sample = 0
    total_ite = 0
    init = True	
    pub = rospy.Publisher('/single_joint_actuator/joint2_position_controller/command', Float64, queue_size=1)
    rospy.init_node('square_wave_generator', anonymous=True)
    rate = rospy.Rate(freq) # hz
    cycle_test = 10
    while not rospy.is_shutdown():
	if init is True:
		amplitude.data = 0.0
	        rospy.loginfo(amplitude)
        	pub.publish(amplitude)
        	rate.sleep()
		init = False
	else: 	
        	if sample <= h and total_ite < cycle_test:
			amplitude.data = a
	        	rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
		elif sample > h and total_ite < cycle_test:
			amplitude.data = -a
			rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
                elif total_ite > cycle_test:
                        amplitude.data = 0.0
                        rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()

		sample +=1
		if sample == 2*h :
                        total_ite +=1 
			sample = 0	#sample variable might be useful in case of sine function
						
		
		
if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass

