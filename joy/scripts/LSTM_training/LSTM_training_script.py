"""
#######################################################################################################################

# This script is train the LSTM network for the hysteresis compensation research

#######################################################################################################################
"""
import sys
sys.path.append('/home/cflai/PycharmProjects/catkin_ws_py/joy/scripts')
import numpy as np
import matplotlib.pyplot as plt

def load_data_from_bag(filename, file_dir):
    print('nothing')

if __name__ == "__main__":
    training_file = 'training.bag'
    validation_file = 'validation.bag'
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


    # TODO: Then I don't need to joint files, but still need to normalize the data collected.
    # TODO: To build bad loader as well!
    # TODO: To decide what input dimensions and output dimensions are!

    encoder_norm, target_x_norm = load_data_from_bag(training_file, file_directory)

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
