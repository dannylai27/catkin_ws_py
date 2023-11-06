#!/usr/bin/env python


import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats



q_1 = 0

def callback_angle_motor_1(callback_angle_motor_1_variable):
    global q_1
    q_1 = callback_angle_motor_1_variable.data[0]


def wave():
    global q_1

    amplitude = Float64()
    freq = 40  # Hz sampling frequency
    a = 0.5 # amplitude square wave
    rad_to_deg = 180.0/3.14
    sample = 0
    total_ite = 0
    init = True	
    pub = rospy.Publisher('/single_joint_actuator/joint1_position_controller/command', Float64, queue_size=1)
    rospy.init_node('square_wave_generator', anonymous=True)
    rospy.Subscriber("/joint_states_from_arduino_1", Floats, callback_angle_motor_1, queue_size=1)
    rate = rospy.Rate(freq) # hz
    cycle_test = 10

    flag = 0

    while not rospy.is_shutdown():
	if init is True:
		amplitude.data = 0.0
	        rospy.loginfo(amplitude)
        	pub.publish(amplitude)
        	rate.sleep()
		init = False
	else: 	
        	if total_ite < cycle_test and flag == 0:
			if not(q_1 < a*rad_to_deg):
				flag = 1
				sample +=1			
			amplitude.data = a
	        	rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
		elif total_ite < cycle_test and flag == 1:
			if not(q_1 > -a*rad_to_deg):
				flag = 0
				sample +=1
			amplitude.data = -a
			rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()
                elif total_ite >= cycle_test:
                        amplitude.data = 0.0
                        rospy.loginfo(amplitude)
        		pub.publish(amplitude)
        		rate.sleep()

		if sample == 2 :
                        total_ite +=1 
			sample = 0	#sample variable might be useful in case of sine function
						
		
		
if __name__ == '__main__':
    try:
        wave()
    except rospy.ROSInterruptException:
        pass

