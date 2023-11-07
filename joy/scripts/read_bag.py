#!/usr/bin/env python3

from bagpy import bagreader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import tensorflow as tf


class ExpResult:
    def __init__(self, f_folder, f_name):
        self.encoders_norm = None
        self.target_y_filter = None
        self.target_x_filter = None
        self.encoders_filter = None
        self.target_x_norm = None
        self.target_y_norm = None
        self.encoders_norm = None
        temp = f_name.split('_')
        print(temp)
        self.label = temp[5] + '_' + temp[6] + temp[7]
        f_dir = f_folder + f_name
        b = bagreader(f_dir)
        motors_states_sync = b.message_by_topic('/motors_states_sync')
        target_centroid_sync = b.message_by_topic('/target_centroid_sync')
        vel_array_sync = b.message_by_topic('/vel_array_sync')
        # time_stamp = b.message_by_topic('/motors_states_sync')
        df_motors_states_sync = pd.read_csv(motors_states_sync)
        df_target_centroid_sync = pd.read_csv(target_centroid_sync)
        df_vel_array_sync = pd.read_csv(vel_array_sync)
        # df_time_stamp = pd.read_csv(time_stamp)

        time_stamp = df_motors_states_sync["Time"].tolist()
        time_stamp = np.array(time_stamp)
        encoders = df_motors_states_sync["data_0"].tolist()
        encoders = np.array(encoders)
        target_x = df_target_centroid_sync["data_0"].tolist()
        target_x = np.array(target_x)
        target_y = df_target_centroid_sync["data_1"].tolist()
        target_y = np.array(target_y)
        vel_array_sync = df_vel_array_sync["data_0"].tolist()
        vel_array_sync = np.array(vel_array_sync)

        if len(target_x) > len(encoders):
            n = len(target_x) - len(encoders)
            target_x = target_x[n:]
            target_y = target_y[n:]
            print('trim data:', self.label)

        elif len(target_x) < len(encoders):
            n = len(encoders) - len(target_x)
            encoders = encoders[n:]
            print('trim data:', self.label)

        # perform data cleaning:
        print('before cleaning, len of target:', len(encoders), len(target_x))
        if sum([i for i in vel_array_sync == 0]) > 4:
            self.zeros_len = sum([i for i in vel_array_sync == 0]) - 3
            self.time_stamp = time_stamp[0:-self.zeros_len]
            self.encoders = encoders[0:-self.zeros_len]
            self.target_x = target_x[0:-self.zeros_len]
            self.target_y = target_y[0:-self.zeros_len]
            self.vel_array_sync = vel_array_sync[0:-self.zeros_len]
            print('after cleaning data, len of target:', len(self.encoders), len(self.target_x))
        else:
            self.time_stamp = time_stamp
            self.encoders = encoders
            self.target_x = target_x
            self.target_y = target_y
            self.vel_array_sync = vel_array_sync
            # print('len of target:', self.encoders, self.target_x)

        self.len = len(time_stamp)
        # n = 4
        # self.encoders = self.encoders[:-n]
        # self.target_x = self.target_x[n:]
        # self.target_y = self.target_y[n:]
        # self.vel_array_sync = self.vel_array_sync[:-n]

    def plot(self, sync_const=0, filter_flag=False):
        fig, ax = plt.subplots()
        data_len = len(self.encoders)
        if filter_flag:
            ax.scatter(self.encoders[0:data_len - sync_const], self.target_x[sync_const:])
            ax.set_title('VS target vs Motor revolution' + '(' + self.label + ')')
            # plt.scatter(self.encoders, self.target_x, label=label)
        else:
            ax.scatter(self.encoders_filter[0:data_len - sync_const], self.target_y_filter[sync_const:])
            ax.set_title('VS target vs Motor revolution' + '(' + self.label + ')')

    def gaussian_filter(self, sigma):
        self.encoders_filter = gaussian_filter1d(self.encoders, sigma)
        self.target_x_filter = gaussian_filter1d(self.target_x, sigma)
        self.target_y_filter = gaussian_filter1d(self.target_y, sigma)
        # return self.encoders_filter, self.target_x_filter, self.target_y_filter

    def stats_1D_array(self, np_array):
        mean = np.mean(np_array)
        std = np.std(np_array)
        return mean, std

    def norm_value(self):
        target_x_mean, target_x_std = stats_1D_array(self.target_x)
        target_y_mean, target_y_std = stats_1D_array(self.target_y)
        encoders_mean, encoders_std = stats_1D_array(self.encoders)
        self.target_x_norm = (self.target_x - target_x_mean) / target_x_std
        self.target_y_norm = (self.target_y - target_y_mean) / target_y_std
        self.encoders_norm = (self.encoders - encoders_mean) / encoders_std

        # def offset_sync(self, n=4):
    #     self.encoders = self.encoders[:-n]
    #     self.target_x = self.target_x[n:]
    #     self.target_y = self.target_y[n:]
    #     self.vel_array_sync = self.vel_array_sync[:-n]

    # def clean_waiting_time(self):


def customized_tanh(x, amp=4):
    return tf.keras.backend.tanh(x) * amp


def create_LSTM_model(feature_width, feature_number=2, cell_number=32, early_stop_patience=5):
    model = tf.keras.Sequential()
    # model.add(tf.keras.layers.LSTM(cell_number, input_shape=(feature_width, feature_number),
    # return_sequence=True) # return_sequence true for all layers except the last one.
    model.add(tf.keras.layers.LSTM(cell_number, input_shape=(feature_width, feature_number)))
    model.add(tf.keras.layers.Dense(1, activation=customized_tanh))
    model.compile(optimizer='adam', loss=tf.losses.MeanSquaredError(), metrics=[tf.metrics.MeanAbsoluteError()])
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=early_stop_patience, mode='min')
    model.summary()

    return model, early_stopping


def create_LSTM_MM_model(feature_width, time_stamp=4, feature_number=2, cell_number=32, early_stop_patience=5):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(cell_number, input_shape=(feature_width, feature_number)))
    model.add(tf.keras.layers.RepeatVector(time_stamp))  # in time stamps
    model.add(tf.keras.layers.LSTM(cell_number, return_sequences=True))
    model.add(
        tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(2, activation=customized_tanh)))  # in feature numbers
    model.compile(optimizer='adam', loss=tf.losses.MeanSquaredError(), metrics=[tf.metrics.MeanAbsoluteError()])
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=early_stop_patience, mode='min')
    model.summary()

    return model, early_stopping


def create_dense_model(conv=False, filters=32, kernel_size=5):
    dense = tf.keras.Sequential()
    if conv is True:
        dense.add(tf.keras.layers.Conv1D(filters=filters, kernel_size=kernel_size))
    else:
        dense.add(tf.keras.layers.Flatten())
    dense.add(tf.keras.layers.Dense(16))
    dense.add(tf.keras.layers.Dense(16))
    dense.add(tf.keras.layers.Dense(1))
    dense.compile(optimizer='adam', loss=tf.losses.MeanSquaredError(), metrics=[tf.metrics.MeanAbsoluteError()])
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3, mode='min')
    # dense.summary()

    return dense, early_stopping


def stats_1D_array(np_array):
    mean = np.mean(np_array)
    std = np.std(np_array)

    return mean, std


def load_bag_files(directory):
    from os import listdir
    from os.path import isfile, join
    training_files = [f for f in listdir(directory + 'training/') if isfile(join(directory + 'training/', f))]
    validation_files = [f for f in listdir(directory + 'validation/') if isfile(join(directory + 'validation/', f))]

    return training_files, validation_files


def load_all_experiments(file_name_list, file_folder, plot=False, sync=True):
    # file_name_list is a list containing bag file directories
    # file folder
    exp_results = []
    if plot:
        fig, ax = plt.subplots()
    for i in file_name_list:
        temp = ExpResult(file_folder, i)
        if sync:
            None
            # temp.offset_sync(n=100)
        if plot:
            ax.scatter(temp.encoders[800:1200], temp.target_x[800:1200], label=temp.label)
        exp_results.append(temp)

    return exp_results


def joint_results(exp_results):
    # calculate stats:
    encoder_all = np.array([])
    target_x_all = np.array([])
    target_y_all = np.array([])
    encoder_norm = np.array([])
    target_x_norm = np.array([])
    target_y_norm = np.array([])
    for result in exp_results:
        encoder_all = np.concatenate((encoder_all, result.encoders), axis=0)
        target_x_all = np.concatenate((target_x_all, result.target_x), axis=0)
        target_y_all = np.concatenate((target_y_all, result.target_y), axis=0)

    encoder_mean, encoder_std = stats_1D_array(encoder_all)
    target_x_all_mean, target_x_all_std = stats_1D_array(target_x_all)
    target_y_all_mean, target_y_all_std = stats_1D_array(target_y_all)

    print('encoder_mean', encoder_mean, 'encoder_std', encoder_std)
    print('x_mean', target_x_all_mean, 'x_std', target_x_all_std)
    print('y_mean', target_y_all_mean, 'y_std', target_y_all_std)

    for result in exp_results:
        temp = (result.encoders - encoder_mean) / encoder_std
        encoder_norm = np.concatenate((encoder_norm, temp), axis=0)

        temp = (result.target_x - target_y_all_mean) / target_x_all_std
        target_x_norm = np.concatenate((target_x_norm, temp), axis=0)

        temp = (result.target_y - target_y_all_mean) / target_y_all_std
        target_y_norm = np.concatenate((target_y_norm, temp), axis=0)

    return encoder_norm, target_x_norm, target_y_norm


# file_dir = [
#     # '10-08-2022_attenuated_a400_T_8_fc_0_15_tc_02_r_2.bag',
#     # '10-08-2022_attenuated_a500_T_10_fc_0_15_tc_02_r_2.bag',
#     '10-08-2022_attenuated_a600_T_12_fc_0_15_tc_02_r_2.bag',
#     # '10-08-2022_attenuated_a500_T_12_fc_0_15_tc_02_r_1.bag',
#     # '10-08-2022_attenuated_a600_T_16_fc_0_15_tc_02_r_1.bag',
#     # '10-08-2022_attenuated_a600_T_16_fc_0_15_tc_02_r_2.bag'
#             ]
if __name__ == "__main__":
    print("Executed when invoked directly")
    a = ExpResult('/home/cflai/temp/', 'pilot_a_inv_cos_t_final_l_monday_siexp_cos1.bag')
    # a.plot(filter_flag=True)
    a.norm_value()
    fig1, ax1 = plt.subplots()
    ax1.plot(a.encoders_norm, a.target_x_norm, 'C1')
    ax1.scatter(a.encoders_norm, a.target_x_norm, s=60, zorder=2.5)
    ax1.set_xlabel('encoder in theta (normalized)')
    ax1.set_ylabel('target in pixel (normalized)')
    ax1.set_title('Hysteresis behaviours')
    fig2, ax2 = plt.subplots()
    ax2.plot(a.encoders, '-o')
    ax2.set_ylabel('encoder in theta (normalized)')
    ax2.set_xlabel('index')
    ax2.set_title('Designed motor movement')
    fig3, ax3 = plt.subplots()
    ax3.plot(a.target_x, '-o')
    ax3.set_xlabel('index')
    ax3.set_ylabel('target in pixel (normalized)')
    ax3.set_title('Visual target')
    plt.show()
    fig4, ax4 = plt.subplots()
    ax4.plot(a.vel_array_sync, '-o')
    ax4.set_xlabel('index')
    ax4.set_ylabel('Rotation speed (step/sec)')
    ax4.set_title('Velocity of the motors')
    plt.show()
    # file_dir = [
    #     '12-08-2022_attenuated_zero_offset_600_a600_T_6_fc_0_15s=120_tc_02_r_1.bag',
    #     '12-08-2022_attenuated_zero_offset_600_a600_T_10_fc_0_15_tc_02_r_1.bag',
    #     '12-08-2022_attenuated_zero_offset_600_a600_T_12_fc_0_15_tc_02_r_1.bag',
    #     '12-08-2022_attenuated_zero_offset_600_a600_T_16_fc_0_15_tc_02_r_1.bag'
    # ]
    #
    # fig, ax = plt.subplots()
    #
    # for exp in file_dir:
    #     exp_result = ExpResult(exp)
    #     ax.scatter(exp_result.encoders, exp_result.target_x, label=exp_result.label)
    #
    # plt.legend()
    # plt.show()

###########
# file_dir_2 = [
#     # '10-08-2022_attenuated_a400_T_8_fc_0_15_tc_02_r_2.bag',
#     '10-08-2022_attenuated_a500_T_10_fc_0_15_tc_02_r_2.bag',
#     # '10-08-2022_attenuated_a600_T_12_fc_0_15_tc_02_r_2.bag',
#     '10-08-2022_attenuated_a500_T_12_fc_0_15_tc_02_r_1.bag',
#     # '10-08-2022_attenuated_a500_T_12_fc_0_15_tc_02_r_2.bag',
#     # '10-08-2022_attenuated_a600_T_16_fc_0_15_tc_02_r_1.bag',
#     # '10-08-2022_attenuated_a600_T_16_fc_0_15_tc_02_r_2.bag'
#             ]
#
# fig2, ax2 = plt.subplots()
#
# for exp in file_dir_2:
#     exp_result = ExpResult(exp)
#     ax2.scatter(exp_result.encoders, exp_result.target_x, label=exp_result.label)
#
# plt.legend()
# plt.show()
