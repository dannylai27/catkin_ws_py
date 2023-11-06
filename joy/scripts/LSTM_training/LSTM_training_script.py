"""
#######################################################################################################################

# This script is train the LSTM network for the hysteresis compensation research

#######################################################################################################################
"""

import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    file_directory = '/home/cflai/catkin_ws_py/src/joy/scripts/LSTM_training/bag/'
    training_option = 'MM_output'
    width = 16
    cell_number = 16
    time_stamp = 4
    save_model_name = 'LSTM_training_dataset_' + \
                      str(training_option) + \
                      '_cell_' + str(cell_number) + \
                      '_width_' + str(width) + \
                      '_t_' + str(time_stamp) + \
                      '.h5'
