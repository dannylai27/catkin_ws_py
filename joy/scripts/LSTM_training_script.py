"""

This script is train the LSTM network for the hysteresis compensation research

"""
import sys
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
from read_bag import create_LSTM_model, ExpResult
from LSTM_function import create_1D_LSTM_dataset
from bagpy import bagreader


class SyncDataLSTM:
    def __init__(self, f_folder, f_name):
        self.encoder_M2_norm = None
        self.encoder_M1_norm = None
        self.target_y_filter = None
        self.target_x_filter = None
        self.encoder_M1_filtered = None
        self.encoder_M2_filtered = None
        self.target_x_norm = None
        self.target_y_norm = None
        self.encoders_norm = None
        self.func_flag = None
        # temp = f_name.split('_')
        # print(temp)
        # self.label = temp[5] + '_' + temp[6] + temp[7]
        f_dir = f_folder + f_name
        b = bagreader(f_dir)

        # TODO: it is important to sort out the right topic for this version.
        motor_M1_sync = b.message_by_topic('/sync/motor_encoder_M1')
        motor_M2_sync = b.message_by_topic('/sync/motor_encoder_M2')
        target_centroid_sync = b.message_by_topic('/sync/target_centroid')
        func_flag_sync = b.message_by_topic('/sync/func_enable_flag')
        df_motor_M1_sync = pd.read_csv(motor_M1_sync)
        df_motor_M2_sync = pd.read_csv(motor_M2_sync)
        df_target_centroid_sync = pd.read_csv(target_centroid_sync)
        df_func_flag_sync = pd.read_csv(func_flag_sync)

        time_stamp = df_motor_M1_sync["Time"].tolist()
        time_stamp = np.array(time_stamp)
        encoder_M1 = df_motor_M1_sync["data"].tolist()  # NOT SURE IF THIS IS "data"!
        encoder_M1 = np.array(encoder_M1)
        encoder_M2 = df_motor_M2_sync["data"].tolist()  # NOT SURE IF THIS IS "data"!
        encoder_M2 = np.array(encoder_M2)
        target_x = df_target_centroid_sync["point.x"].tolist()
        target_x = np.array(target_x)
        target_y = df_target_centroid_sync["point.y"].tolist()
        target_y = np.array(target_y)
        func_flag = df_func_flag_sync["data"].tolist()
        func_flag = np.array(func_flag)


        # This is to take off those points which are not synchornized in the end of array.
        if len(target_x) > len(encoder_M1):
            n = len(target_x) - len(encoder_M1)
            target_x = target_x[n:]
            target_y = target_y[n:]
            print('trim data:', self.label)

        elif len(target_x) < len(encoder_M1):
            n = len(encoder_M1) - len(target_x)
            encoder_M1 = encoder_M1[n:]
            print('trim data:', self.label)

        # perform data cleaning, to avoid training with dataset with:
        # using flag to avoid too early recording / too late recording when using bag record.
        self.time_stamp = time_stamp[func_flag]
        self.encoder_M1 = encoder_M1[func_flag]
        self.encoder_M2 = encoder_M2[func_flag]
        self.target_x = target_x[func_flag]
        self.target_y = target_y[func_flag]
        self.len = len(self.time_stamp)
        print(len(time_stamp) - self.len, ' data points are removed')


    # TODO: temporarily I disable the  plot function as the file name is not determined yet.
    ##################################################################################################
    # def plot(self, sync_const=0, filter_flag=False):
    #     fig, ax = plt.subplots()
    #     data_len = len(self.encoder_M1)
    #     if filter_flag:
    #         ax.scatter(self.encoder_M1[0:data_len - sync_const], self.target_x[sync_const:])
    #         ax.set_title('VS target vs Motor revolution' + '(' + self.label + ')')
    #         # plt.scatter(self.encoder_M1, self.target_x, label=label)
    #     else:
    #         ax.scatter(self.encoder_M1_filtered[0:data_len - sync_const], self.target_y_filter[sync_const:])
    #         ax.set_title('VS target vs Motor revolution' + '(' + self.label + ')')
    ##################################################################################################

    def gaussian_filter(self, sigma):
        self.encoder_M1_filtered = gaussian_filter1d(self.encoder_M1, sigma)
        self.encoder_M2_filtered = gaussian_filter1d(self.encoder_M2, sigma)
        self.target_x_filter = gaussian_filter1d(self.target_x, sigma)
        self.target_y_filter = gaussian_filter1d(self.target_y, sigma)
        # return self.encoder_M1_filtered, self.target_x_filter, self.target_y_filter

    def stats_1D_array(self, np_array):
        mean = np.mean(np_array)
        std = np.std(np_array)
        return mean, std

    def norm_value(self):
        target_x_mean, target_x_std = self.stats_1D_array(self.target_x)
        target_y_mean, target_y_std = self.stats_1D_array(self.target_y)
        encoder_M1_mean, encoder_M1_std = self.stats_1D_array(self.encoder_M1)
        encoder_M2_mean, encoder_M2_std = self.stats_1D_array(self.encoder_M2)
        self.target_x_norm = (self.target_x - target_x_mean) / target_x_std
        self.target_y_norm = (self.target_y - target_y_mean) / target_y_std
        self.encoder_M1_norm = (self.encoder_M1 - encoder_M1_mean) / encoder_M1_std
        self.encoder_M2_norm = (self.encoder_M2 - encoder_M2_mean) / encoder_M2_std

        return


def load_data_from_bag(file_dir, file_name):
    Result = SyncDataLSTM(file_dir, file_name)
    Result.norm_value()
    feature_norm = Result.encoder_M1_norm
    label_norm = Result.target_x_norm
    return feature_norm, label_norm


if __name__ == "__main__":
    training_file = 'bag_with_less_shits1.bag'
    validation_file = 'bag_with_less_shits2.bag'
    file_directory = '/home/cflai/catkin_ws_py/src/joy/scripts/LSTM_training/bag/'
    training_option = 'one_feature'
    width = 16
    cell_number = 16
    time_stamp = 4
    save_model_name = 'LSTM_training_dataset_' + \
                      str(training_option) + \
                      '_cell_' + str(cell_number) + \
                      '_width_' + str(width) + \
                      '_t_' + str(time_stamp) + \
                      '.h5'

    # TODO: Should I collect all the data in one recording?  ANS on 06112023 is: YES!
    # So first, let's build this script with the assumption that I will have only one bag!

    # TODO: To decide what input dimensions and output dimensions are!

    encoder_norm, target_x_norm = load_data_from_bag(file_directory, training_file)
    encoder_norm_validation, target_x_norm_validation = load_data_from_bag(file_directory, validation_file)

    # Options for LSTM model building
    if training_option == 'one_feature':
        feature_number = 1
        features, labels, labels_x = create_1D_LSTM_dataset(encoder_norm, target_x_norm, feature_width=width)
        features_validation, labels_validation, labels_x_validation = create_1D_LSTM_dataset(encoder_norm_validation,
                                                                                             target_x_norm_validation,
                                                                                             feature_width=width)
        print('one feature training created')
        LSTM_model, early_stopping = create_LSTM_model(feature_width=width,
                                                       feature_number=feature_number,
                                                       cell_number=cell_number,
                                                       early_stop_patience=5)

    # Starts to fit/feed/train the LSTM network from previously constructed data
    LSTM_model.fit(features, labels, epochs=400, batch_size=64,
                   callbacks=[early_stopping],
                   validation_data=(features_validation, labels_validation))

    LSTM_model.save(file_directory + save_model_name)
    prediction_LSTM = LSTM_model.predict(features)


    # This is the plotting section:
    fig, axs = plt.subplots(1, 2)
    if training_option == ('one_feature' or 'two_features'):
        a = 0
        b = 100
        axs[0].plot(np.squeeze(prediction_LSTM[a:a + b]), marker='x')
        axs[0].plot(np.squeeze(labels[a:a + b]), marker='o')
        axs[1].plot(encoder_norm[a:a + b])
        axs[1].plot(target_x_norm[a:a + b])

        plt.legend()
        plt.show()

    elif training_option == 'MM_output':
        def plot_MM(n):
            fig2, ax = plt.subplots(1, 4)

            for i in range(4):
                pre = np.transpose(features[n + 20 * i])
                fut = np.transpose(prediction_LSTM[n + 20 * i])
                gt = np.transpose(labels[n + 20 * i])
                ax[i].plot(pre[0], pre[1], marker='o')
                ax[i].plot(fut[0], fut[1], marker='x')
                ax[i].plot(gt[0], gt[1], marker='^')

            plt.legend()
            plt.show()

            return
        plot_MM(120)
