from bagpy import bagreader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from read_bag import create_LSTM_model, create_dense_model, joint_results, load_all_experiments, load_bag_files, \
    create_LSTM_MM_model
from LSTM_function import create_LSTM_dataset, create_1D_LSTM_dataset, create_LSTM_MM_dataset
import tensorflow as tf
import h5py

# GOOD DATA from attenuated ####
# 10-08-2022_attenuated_a400_T_8_fc_0_15_tc_02_r_2.bag
# 10-08-2022_attenuated_a500_T_10_fc_0_15_tc_02_r_2.bag
# 10-08-2022_attenuated_a600_T_12_fc_0_15_tc_02_r_2.bag

if __name__ == "__main__":
    file_directory = '/home/cflai/catkin_ws_py/bag_file/VS_exp/x_axis_28102022/'
    training_option = 'MM_output'
    # option = 'one_feature'
    # option = 'one_features'
    width = 16
    cell_number = 16
    time_stamp = 4
    save_model_name = 'LSTM_training_dataset_28102022_' + \
                      str(training_option) + \
                      '_cell_' + str(cell_number) + \
                      '_width_' + str(width) + \
                      '_t_' + str(time_stamp) + \
                      '.h5'

    # print(file_dir[0])
    #
    # exp_result = read_bag.ExpResult(file_directory, file_dir[0])

    file_dir_training, file_dir_validation = load_bag_files(file_directory)
    exp_results = load_all_experiments(file_dir_training, file_directory + 'training/')
    exp_results_validation = load_all_experiments(file_dir_validation, file_directory + 'validation/')
    encoder_norm, target_x_norm, target_y_norm = joint_results(exp_results)
    encoder_norm_validation, target_x_norm_validation, target_y_norm_validation = joint_results(exp_results_validation)

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

    elif training_option == 'two_features':
        feature_number = 2
        features, labels, labels_x = create_LSTM_dataset(encoder_norm, target_x_norm,
                                                         feature_width=width,
                                                         label_width=1)
        features_validation, labels_validation, labels_x_validation = create_LSTM_dataset(encoder_norm_validation,
                                                                                          target_x_norm_validation,
                                                                                          feature_width=width,
                                                                                          label_width=1)
        print('two feature training created')
        LSTM_model, early_stopping = create_LSTM_model(feature_width=width,
                                                       feature_number=feature_number,
                                                       cell_number=cell_number,
                                                       early_stop_patience=5)

    elif training_option == 'MM_output':
        feature_number = 2
        features, labels, labels_x = create_LSTM_MM_dataset(encoder_norm, target_x_norm,
                                                            feature_width=width,
                                                            label_width=time_stamp)
        features_validation, labels_validation, labels_x_validation = create_LSTM_MM_dataset(encoder_norm_validation,
                                                                                             target_x_norm_validation,
                                                                                             feature_width=width,
                                                                                             label_width=time_stamp)
        print('MM features training created')
        LSTM_model, early_stopping = create_LSTM_MM_model(feature_width=width,
                                                          time_stamp=time_stamp,
                                                          feature_number=feature_number,
                                                          cell_number=cell_number,
                                                          early_stop_patience=5)

    else:
        raise Exception('Please select the right feature options')

    LSTM_model.fit(features, labels, epochs=400, batch_size=64,
                   callbacks=[early_stopping],
                   validation_data=(features_validation, labels_validation))
    LSTM_model.save(file_directory + save_model_name)
    prediction_LSTM = LSTM_model.predict(features)

    fig, axs = plt.subplots(1, 2)
    if training_option == ('one_feature' or 'two_features'):
        a = 1200
        b = 400
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


    # LSTM_ROS.fit(features, labels, epochs=200, batch_size=8, callbacks=[early_stopping], validation_data=(
    # validation_feature_set_list, validation_label_set_list))

    ################################

    """ Plot SECTION
    plt.figure(dpi=180)
    # plt.scatter(time_stamp_M[100:130], encoders[100:130], marker='x', label='motor')
    # plt.scatter(time_stamp_T[70:110], target_x[70:110], marker='x', label='CV')
    
    # plt.scatter(encoders, target_x, label='y')
    plt.scatter(encoders[0:-2], target_x[2:], label='f_1')
    plt.legend()
    # plt.scatter(encoders, target_y, label='y')
    plt.show()
    END of Plot"""
