#!/usr/bin/env python


import rospy
from std_msgs.msg import Float64




def wave():

    amplitude = Float64()
    freq = 40  # Hz sampling frequency
    T0 = 10
    half_period = T0 # in seconds, frequency of the square wave (2*half_period)^(-1)
    h = freq*half_period
    
    s = 0
    m = 0.002 # slope of the ramp, the signal will be a ramp of amplitude proportional to the period
    a = 0.0 # considering Tmax = 20s we have 10*40*m= max ramp amplitude, setting m = 0.002 we have 400*0.002 = 0.8
    T1 = 5
    n1 = 5 
    T2 = 2
    n2 = 10
    T3 = 1
    n3 = 15
    n4 = 20
    

    sample = 0
    total_ite = 0
    init = True	
    pub = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)
    rospy.init_node('square_wave_generator', anonymous=True)
    rate = rospy.Rate(freq) # hz
    cycle_test = 25
    while not rospy.is_shutdown():
	if init is True:
		amplitude.data = 0.0
	        rospy.loginfo(amplitude)
        	pub.publish(amplitude)
        	rate.sleep()
		init = False
	else: 	
        	if sample <= h and total_ite < cycle_test:
			amplitude.data = s*m
			s = s+1
	        	rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
		elif sample > h and total_ite < cycle_test:
			amplitude.data = -s*m
			s = s+1
			rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
                elif total_ite > cycle_test:
                        amplitude.data = 0.0
                        rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()


		sample +=1
		
		if (sample == h):
			s = 0
		
		if sample == 2*h :
                        total_ite +=1 
			sample = 0	#sample variable might be useful in case of sine function
                      
		if (sample == 0):
			s = 0		

		if total_ite>n1:
			half_period = T1
    			h = freq*half_period
		elif total_ite>n2:
			half_period = T2
			h = freq*half_period
		elif total_ite>n3:
			half_period = T3
			h = freq*half_period
		elif total_ite>n4:
			half_period = T0
 			h = freq*half_period
				
						
		
		
if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass

