import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
# from read_bag import load_all_experiments
from bagpy import bagreader
import pandas as pd
import numpy as np

def trial_plot():

    setpoint = bag_list[0].message_by_topic('/desired_trajectory_CV')
    error = bag_list[0].message_by_topic('/p_error')
    jacobian_val = bag_list[0].message_by_topic('/predicted_jacobian_value')
    vel_mock = bag_list[0].message_by_topic('/vel_array_mock')
    df_setpoint = pd.read_csv(setpoint)
    df_error = pd.read_csv(error)
    df_jacobian = pd.read_csv(jacobian_val)
    df_vel_mock = pd.read_csv(vel_mock)

    df_setpoint.plot(kind='scatter', x='Time', y='data')
    df_error.plot(kind='scatter', x='Time', y='data')
    df_jacobian.plot(kind='scatter', x='Time', y='data')
    df_vel_mock.plot(kind='scatter', x='Time', y='data_0')

    plt.show()

    return df_setpoint, df_error, df_jacobian, df_vel_mock


def Q_CV_plot(bag_list):

    norm_val = bag_list[0].message_by_topic('/norm_val')
    error = bag_list[0].message_by_topic('/p_error')
    target_pos = bag_list[0].message_by_topic('/target_centroid')
    df_norm_val = pd.read_csv(norm_val)
    df_error = pd.read_csv(error)
    df_target_pos = pd.read_csv(target_pos)

    df_norm_val.plot(kind='scatter', x='Time', y='data')
    df_error.plot(kind='scatter', x='Time', y='data')
    df_target_pos.plot(kind='scatter', x='Time', y='data')

    plt.show()

    return df_norm_val, df_error, df_target_pos


if __name__ == "__main__":

    file_folder = '/home/cflai/catkin_ws_py/bag_file/norm_val/'
    trial_files = [f for f in listdir(file_folder) if isfile(join(file_folder, f))]
    # trial_results = load_all_experiments(file_folder, file_folder + 'validation/')

    for name in trial_files:
        bag_list = []
        b = bagreader(file_folder+name)
        bag_list.append(b)
        print(name)

    norm_val = bag_list[0].message_by_topic('/norm_val')
    # error = bag_list[0].message_by_topic('/p_error')
    # target_pos = bag_list[0].message_by_topic('/target_centroid')
    df_norm_val = pd.read_csv(norm_val)
    # df_error = pd.read_csv(error)
    # df_target_pos = pd.read_csv(target_pos)

    df_norm_val.plot(x='Time', y=['data_0', 'data_1', 'data_2', 'data_3', 'data_4'], title='all_data')
    plt.legend(['cv_new', 'cv_old', 'q_new', 'q_old', 'j'])
    df_norm_val.plot(x='data_1', y=['data_2', 'data_3'], title='cv_vs_q (normalized)')
    plt.legend(['q_new', 'q_old'])
    plt.xlabel('cv(pixels)')
    plt.ylabel('q(theta)')


    # df_error.plot(kind='scatter', x='Time', y='data')
    # df_target_pos.plot(kind='scatter', x='Time', y='data')

    plt.show()




