#!/usr/bin/env python3

"""
#######################################################################################################################

# This script is used to synchronize the following data for data collection!
    /sync/target_centroid, PointStamped,
    /sync/setpoint_M1, Float64,
    /sync/motor_encoder_M1, Float64,
    /sync/setpoint_M2, Float64,
    /sync/motor_encoder_M2, Float64,

#######################################################################################################################
"""

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import PointStamped


class SyncDataFlexy:
    def __init__(self, target_x, target_y, motor_x, motor_y, ros_time):
        self.target_x = target_x
        self.target_y = target_y
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.ros_time = ros_time


class RecordedDataFlexy:
    def __init__(self, load_data_flag=False):
        if load_data_flag:
            pass
        else:
            self.target_x_list = []
            self.target_y_list = []
            self.motor_x_list = []
            self.motor_y_list = []
            self.time_list = []
        self.data_list = [self.target_x_list, self.target_y_list, self.motor_x_list, self.motor_y_list]
        self.data_list_name = ['target_x', 'target_y', 'motor_x', 'motor_y']

    def append(self, Data):
        self.target_x_list.append(Data.target_x)
        self.target_y_list.append(Data.target_y)
        self.motor_x_list.append(Data.motor_x)
        self.motor_y_list.append(Data.motor_y)
        self.time_list.append(Data.ros_time)

    def plot(self):
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(4, 1)
        # We are drawing for all the recording data respect to time!
        for data, ax, name in zip(self.data_list, axes, self.data_list_name):
            ax.plot(self.time_list, data, label=name)
            ax.legend()
        plt.show()

    def save(self, filename="recorded_data"):
        from numpy import savetxt
        txt_rows = [self.target_x_list, self.target_y_list, self.motor_x_list, self.motor_y_list, self.time_list]
        savetxt(filename+".csv", txt_rows, delimiter=", ", fmt='% s')

    def __str__(self):
        return str(self.data_list_name)


global pub_target_centroid, pub_setpoint_M1, pub_setpoint_M2, \
    pub_encoder_M1, pub_encoder_M2
encoder_M1_sync = Float64()
encoder_M1_sync.data = 0.0
encoder_M2_sync = Float64()
encoder_M2_sync.data = 0.0
setpoint_M1_sync = Float64()
setpoint_M1_sync.data = 0.0
setpoint_M2_sync = Float64()
setpoint_M2_sync.data = 0.0
a = PointStamped()
DataRecorded = RecordedDataFlexy()


def time_stamp2time(point_stamped):
    sec = float(point_stamped.header.stamp.secs)
    nan_sec = float(point_stamped.header.stamp.nsecs)
    float_time = sec + nan_sec * 10 ** (-9)
    return float_time


def callback_syn(data):
    global DataRecorded
    pub_target_centroid.publish(data)
    pub_setpoint_M1.publish(setpoint_M1_sync)
    pub_setpoint_M2.publish(setpoint_M2_sync)
    pub_encoder_M1.publish(encoder_M1_sync)
    pub_encoder_M2.publish(encoder_M2_sync)
    Data = SyncDataFlexy(data.point.x, data.point.y, encoder_M1_sync.data, encoder_M2_sync.data,
                         time_stamp2time(data))
    DataRecorded.append(Data)


def callback_save(data):
    global encoder_M1_sync
    encoder_M1_sync.data = data.data


def callback_save_2(data):
    global setpoint_M1_sync
    setpoint_M1_sync.data = data.data


def callback_save_3(data):
    global encoder_M2_sync
    encoder_M2_sync.data = data.data


def callback_save_4(data):
    global setpoint_M2_sync
    setpoint_M2_sync.data = data.data


def listener():
    global pub_target_centroid, pub_setpoint_M1, pub_setpoint_M2, pub_encoder_M1, pub_encoder_M2
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('data_synchronizer', anonymous=True)
    rate = rospy.Rate(60)
    pub_target_centroid = rospy.Publisher('/sync/target_centroid', PointStamped, queue_size=2)
    pub_setpoint_M1 = rospy.Publisher('/sync/setpoint_M1', Float64, queue_size=2)
    pub_encoder_M1 = rospy.Publisher('/sync/motor_encoder_M1', Float64, queue_size=2)
    pub_setpoint_M2 = rospy.Publisher('/sync/setpoint_M2', Float64, queue_size=2)
    pub_encoder_M2 = rospy.Publisher('/sync/motor_encoder_M2', Float64, queue_size=2)
    rospy.Subscriber("/target_centroid", PointStamped, callback_syn)
    rospy.Subscriber("/motor_encoder_M1", Float64, callback_save)
    rospy.Subscriber("/setpoint_M1", Float64, callback_save_2)
    rospy.Subscriber("/motor_encoder_M2", Float64, callback_save_3)
    rospy.Subscriber("/setpoint_M2", Float64, callback_save_4)
    # TODO: build a try/except to guarantee all the subscriber are getting new messages
    while not rospy.is_shutdown():
        # print('hi')
        rate.sleep()

    DataRecorded.plot()
    DataRecorded.save()


if __name__ == '__main__':
    listener()
