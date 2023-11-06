#!/usr/bin/env python3
import rospy
from rospy_tutorials.msg import Floats

global pub, pub2, pub3
motors_states_sync = Floats()
motors_states_sync.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
vel_array_sync = Floats()
vel_array_sync.data = [0.0, 0.0, 0.0, 0.0, 0.0]
all_sync = Floats()
all_sync.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def callback_syn(data):
    global pub, pub2, pub3, motors_states_sync, all_sync, pub4
    a = motors_states_sync
    b = vel_array_sync
    pub.publish(data)
    pub2.publish(a)
    pub3.publish(b)

    # all_sync.data = data.data + motors_states_sync.data + vel_array_sync.data
    # pub4.publish(all_sync)


def callback_save(data):
    global motors_states_sync
    motors_states_sync.data = data.data


def callback_save_2(data):
    global vel_array_sync
    vel_array_sync.data = data.data


def listener():
    global pub, pub2, pub3
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('data_synchronizer', anonymous=True)
    pub = rospy.Publisher('target_centroid_sync', Floats, queue_size=2)
    pub2 = rospy.Publisher('motors_states_sync', Floats, queue_size=2)
    pub3 = rospy.Publisher('vel_array_sync', Floats, queue_size=2)
    pub4 = rospy.Publisher('all_sync', Floats, queue_size=2)
    rospy.Subscriber("/target_centroid", Floats, callback_syn)
    rospy.Subscriber("/motors_states", Floats, callback_save)
    rospy.Subscriber("/vel_array", Floats, callback_save_2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
