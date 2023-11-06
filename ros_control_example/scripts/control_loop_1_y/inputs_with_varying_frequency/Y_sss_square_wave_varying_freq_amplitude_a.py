#!/usr/bin/env python


#import rospy
#from std_msgs.msg import Float64




#def wave():

#    amplitude = Float64()
#    freq = 40  # Hz sampling frequency
#    a = 0.7 # amplitude square wave
#    half_period = 10 # in seconds, frequency of the square wave (2*half_period)^(-1)
#    h = freq*half_period
#    sample = 0
#    total_ite = 0
#    init = True	
#    pub = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)
#    rospy.init_node('square_wave_generator', anonymous=True)
#    rate = rospy.Rate(freq) # hz
#    cycle_test = 10
#    while not rospy.is_shutdown():
#	if init is True:
#		amplitude.data = 0.0
#	        rospy.loginfo(amplitude)
#        	pub.publish(amplitude)
#        	rate.sleep()
#		init = False
#	else: 	
#        	if sample <= h and total_ite < cycle_test:
#			amplitude.data = a
#	        	rospy.loginfo(amplitude)
#        		pub.publish(amplitude)
#        		rate.sleep()
#		elif sample > h and total_ite < cycle_test:
#			amplitude.data = -a
#			rospy.loginfo(amplitude)
#        		pub.publish(amplitude)
#        		rate.sleep()
#                elif total_ite > cycle_test:
#                        amplitude.data = 0.0
#                        rospy.loginfo(amplitude)
#        		pub.publish(amplitude)
#        		rate.sleep()
#
#		sample +=1
#		if sample == 2*h :
#                        total_ite +=1 
#			sample = 0	#sample variable might be useful in case of sine function
#						
		
		
#if __name__ == '__main__':
#    try:
#        wave()
#    except rospy.ROSInterruptException:
#        pass



#########!/usr/bin/env python

'''
import rospy
from std_msgs.msg import Float64




def wave():

    amplitude = Float64()
    freq = 40  # Hz sampling frequency
    a = 0.7 # amplitude square wave
    T0 = 10
    half_period = T0 # in seconds, frequency of the square wave (2*half_period)^(-1)
    h = freq*half_period
    
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


from random import randint

x = [randint(0, 9) for p in range(0, 10)]



'''

'''
import rospy
from std_msgs.msg import Float64
from random import randint

x = [randint(0, 9) for p in range(0, 10)]



def wave():

    amplitude = Float64()
    freq = 40  # Hz sampling frequency
    a = 0.5 # amplitude square wave
    T0 = 20
    half_period = T0 # in seconds, frequency of the square wave (2*half_period)^(-1)
    h0 = freq*half_period
    h = freq*half_period   
 
#    x = randint(1, 10)
#    y = randint(1, 10) 
#    x1 = x/10.0*T0
#    delay = 0
#    zed = randint(1, 10000)

    sample = 0
    total_ite = 0
    init = True	
    pub = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)
    rospy.init_node('square_wave_generator', anonymous=True)
    rate = rospy.Rate(freq) # hz
    cycle_test =1000
    while not rospy.is_shutdown():
	if init is True:
		amplitude.data = 0.0
	        rospy.loginfo(amplitude)
        	pub.publish(amplitude)
        	rate.sleep()
		init = False
	else: 	
		
#    		if h>=0:
#			h = h + randint(1,3) - randint(1, 3)

#			zed = randint(1, 10000)
#			delay = 0
#    			x1 = x/10.0*T0
#			half_period = x1
#			if half_period > :
#				h = freq*half_period

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


		sample = sample+randint(1,50) 
		if sample >= 2*h :
                        total_ite +=1 
			sample = 0	#sample variable might be useful in case of sine function

				
						
		
		
if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass
'''
'''

import rospy
from std_msgs.msg import Float64
from random import randint



def wave():

    amplitude = Float64()
    freq = 40  # Hz sampling frequency
    a = 0.7 # amplitude square wave

    T = [1,2,3,4,5,6,7,8,9,10]
    T0 = T[randint(0,9)]
    half_period = T0 # in seconds, frequency of the square wave (2*half_period)^(-1)
    h = freq*half_period
    
    
    


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
			half_period = T[randint(0,9)] 
    			h = freq*half_period
                        total_ite +=1 
			sample = 0	#sample variable might be useful in case of sine function

				
						
		
		
if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass


# random.randint(a, b)
#    Return a random integer N such that a <= N <= b


'''

import rospy
from std_msgs.msg import Float64
from random import randint



def wave():

    amplitude = Float64()
    freq = 40  # Hz sampling frequency
    a = 0.7 # amplitude square wave

    T = [3,4,5,6,7,8,9,10]
    T0 = T[randint(0,7)]
    half_period = T0 # in seconds, frequency of the square wave (2*half_period)^(-1)
    h = freq*half_period
    
    
    


    sample = 0
    total_ite = 0
    init = True	
    pub = rospy.Publisher('/single_joint_actuator/joint2_position_controller/command', Float64, queue_size=1)
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


		sample = sample + randint(0,3)
		if sample >= 2*h :
			half_period = T[randint(0,7)] 
    			h = freq*half_period
                        total_ite +=1 
			sample = 0	#sample variable might be useful in case of sine function

				
						
		
		
if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass




