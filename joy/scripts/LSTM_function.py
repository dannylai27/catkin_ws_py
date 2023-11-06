from bagpy import bagreader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view
from scipy.ndimage import gaussian_filter1d


def filter_upper_lower_bound(cv_x, q_x, upper_bound, lower_bound):
    cv_filter = np.array([])
    q_filter = np.array([])

    for i in range(len(q_x)):
        if q_x[i] < upper_bound and q_x[i] > lower_bound:
            q_filter = np.append(q_filter, q_x[i])
            cv_filter = np.append(cv_filter, cv_x[i])

    return cv_filter, q_filter


def create_LSTM_dataset(x, y, feature_width=5, label_width=1, filter=True, filter_sigma=1):
    # x and y should be numpy array
    # x and y should be numpy array
    # x and y are both feature array
    # y is the label
    if filter:
        y = gaussian_filter1d(y, filter_sigma)

    joint_features = np.transpose(np.array([x, y]))
    label = np.transpose(np.array([y]))
    features = sliding_window_view(joint_features[:-label_width], (feature_width, 2))
    # print('features shape before squeeze', features.shape)
    features = np.squeeze(features, axis=1)
    # print('features shape after squeeze', features.shape)

    # create labels:
    if label_width > 1:
        labels = sliding_window_view(label[feature_width:], (label_width, 1))
        labels = np.squeeze(labels)

    elif label_width == 1:
        labels = np.array(joint_features[feature_width:]).reshape(-1, 1, 2)[:, :, 1]

    else:
        raise Exception("label_width should be greater than 0")
    labels_x = np.array(joint_features[feature_width:]).reshape(-1, 1, 2)[:, :, 0]
    # print('labels_x shpae after squeeze', labels_x.shape)

    print("shape of features:", features.shape)
    print("shape of labels:", labels.shape)
    print("shape of labels:", labels_x.shape)
    return features, labels, labels_x


def create_1D_LSTM_dataset(x, y, feature_width=5, label_width=1, filter=True, filter_sigma=2):
    # x and y should be numpy array
    # x is the feature
    # y is the label
    if filter:
        y = gaussian_filter1d(y, filter_sigma)

    joint_features = np.transpose(np.array([x, y]))
    one_feature = np.transpose(np.array([x]))
    label = np.transpose(np.array([y]))
    features = sliding_window_view(one_feature[:-label_width], (feature_width, 1))
    features = np.squeeze(features, axis=1)

    # create labels:
    if label_width > 1:
        labels = sliding_window_view(label[feature_width:], (label_width, 1))
        labels = np.squeeze(labels)

    elif label_width == 1:
        # is this the only way to create width 1 feature?
        labels = np.array(joint_features[feature_width:]).reshape(-1, 1, 2)[:, :, 1]  # so 1 is the feature...?

    else:
        raise Exception("label_width should be greater than 0")
    labels_x = np.array(joint_features[feature_width:]).reshape(-1, 1, 2)[:, :, 0]

    print("First features element:", features[0], "shape of features:", features.shape)
    print("First labels element:", labels[0], "shape of labels:", labels.shape)
    print("First labels_x element:", labels_x[0], "shape of labels:", labels_x.shape)

    return features, labels, labels_x


def create_LSTM_MM_dataset(x, y, feature_width=5, label_width=1, filter=True, filter_sigma=2):
    # Multivariate and Multi-step dataset
    # x and y should be numpy array
    # x and y should be numpy array
    # x and y are both feature array
    # y is the label
    # width means how many time-steps
    # length means how many data in one time-step
    if filter:
        y = gaussian_filter1d(y, filter_sigma)

    joint_features = np.transpose(np.array([x, y]))
    features = sliding_window_view(joint_features[:-label_width], (feature_width, 2))
    # print('features shape before squeeze', features.shape)
    features = np.squeeze(features, axis=1)
    # print('features shape after squeeze', features.shape)

    # create labels:
    if label_width > 1:
        label = np.transpose(np.array([x, y]))
        print('label shape for test:', label.shape)
        labels = sliding_window_view(label[feature_width:], (label_width, label.shape[1]))
        labels = np.squeeze(labels)

    elif label_width == 1:
        labels = np.array(joint_features[feature_width:]).reshape(-1, 1, 2)[:, :, 1]

    else:
        raise Exception("label_width should be greater than 0")
    labels_x = np.array(joint_features[feature_width:]).reshape(-1, 1, 2)[:, :, 0]
    # print('labels_x shpae after squeeze', labels_x.shape)

    print("shape of features:", features.shape)
    print("shape of labels:", labels.shape)
    print("shape of labels:", labels_x.shape)
    return features, labels, labels_x

def split_data(data):
    n = len(data)
    train_data = data[0:int(n * 0.7)]
    val_data = data[int(n * 0.7):int(n * 0.9)]
    test_data = data[int(n * 0.9):]
    return train_data, val_data, test_data


def df_normalize_data(df):
    mean = df.mean()
    std = df.std()
    df_normalize = (df - mean) / std

    # print('mean:', mean)
    # print('std:', std)

    return df_normalize


def normalize_data(data_arrays):
    normalized_array = np.empty((0, len(data_arrays[0])))
    for data in data_arrays:
        # print(data.size)
        mean_value = np.mean(data)
        std_value = np.std(data)
        data = (data - mean_value) / std_value
        normalized_array = np.append(normalized_array, data, axis=0)
    # print(normalized_array.size)
    return normalized_array


def df_clean_data(df, column_index, time_index, nantime_index, bound_index, upper_bound=37, lower_bound=-37):
    # df.append( df.iloc[-1] )
    df['s_sec'] = df[time_index].shift(-1)
    df['s_nan_sec'] = df[nantime_index].shift(-1)
    df['q_pass'] = df['data_6'].shift(-1)
    # print(df.shape)
    # df_clean = df[df[column_index]!=1000&((df[time_index]!=df['s_sec'])|(df[nantime_index]!=df['s_nan_sec']))]
    df_clean = df[(df[column_index] != 1000) & ((df['data_9'] != df['s_nan_sec']) | (df['data_8'] != df['s_sec']))]
    df_clean = df_clean[df_clean['data_6'] != df_clean['q_pass']]
    df_filter = df_clean[(df_clean[bound_index] < upper_bound) & (df_clean[bound_index] > lower_bound)]
    df_filter = df_filter.drop(['s_sec', 's_nan_sec'], axis=1)

    # print(df_clean.shape)
    # print(df_filter.shape)
    return df_filter


def clean_data(q, cv, t, t_nan):
    cv_buff = cv
    q_buff = q
    count = 0
    for i in range(len(cv) - 1):
        if cv[i + 1] != 1000 and (t[i] != t[i + 1] or t_nan[i] != t_nan[i + 1]):
            cv_buff[count] = cv[i + 1]
            q_buff[count] = q[i + 1]
            count = count + 1

    return q_buff[:count - 1], cv_buff[:count - 1]


class LSTMDataset:
    def __init__(self, dataset):
        n = len(dataset)
        self.training = dataset[0:int(n * 0.7)]
        self.validation = dataset[int(n * 0.7):int(n * 0.9)]
        self.testing = dataset[int(n * 0.9)]


def dataset_generation(file_directory, feature_width=5, label_width=5, filter=True, filter_sigma=2, interval=1):
    training_feature_set_list = np.empty((0, feature_width, 2))
    validation_feature_set_list = np.empty((0, feature_width, 2))
    testing_feature_set_list = np.empty((0, feature_width, 2))

    training_label_set_list = np.empty((0, label_width))
    validation_label_set_list = np.empty((0, label_width))
    testing_label_set_list = np.empty((0, label_width))

    training_groundTruth_set_list = np.empty((0, 1))
    validation_groundTruth_set_list = np.empty((0, 1))
    testing_groundTruth_set_list = np.empty((0, 1))

    interval = int(interval)

    for directory in file_directory:
        # bag file to csv:
        b = bagreader(directory)
        error_and_data_MSG = b.message_by_topic('/error_and_data_for_error_computation_test')
        # csv to pd to list:
        df_raw = pd.read_csv(error_and_data_MSG)
        # clean data
        df_clean = df_clean_data(df_raw, 'data_2', 'data_8', 'data_9', 'data_6')
        # normalize data
        df = df_normalize_data(df_clean)

        # read data
        list_cam_x = df['data_2'].tolist()
        list_q_1 = df['data_6'].tolist()
        list_cam_y = df['data_3'].tolist()
        list_q_2 = df['data_7'].tolist()
        list_t_sec = df['data_8'].tolist()
        list_t_nsec = df['data_9'].tolist()

        if filter:
            cv_x = gaussian_filter1d(list_cam_x, filter_sigma)
            q_x = gaussian_filter1d(list_q_1, filter_sigma)

        else:
            cv_x = list_cam_x
            q_x = list_q_1

        cv_x_train, cv_x_validation, cv_x_testing = split_data(cv_x)
        q_x_train, q_x_validation, q_x_testing = split_data(q_x)

        # Create LSTM datset
        features_train, labels_train, labels_x_train = create_LSTM_dataset(cv_x_train, q_x_train, feature_width,
                                                                           label_width=label_width, filter=False)
        features_validation, labels_validation, labels_x_validation = create_LSTM_dataset(cv_x_validation,
                                                                                          q_x_validation, feature_width,
                                                                                          label_width=label_width,
                                                                                          filter=False)
        features_testing, labels_testing, labels_x_testing = create_LSTM_dataset(cv_x_testing, q_x_testing,
                                                                                 feature_width, label_width=label_width,
                                                                                 filter=False)

        # print('test:', features_train.shape)

        training_feature_set_list = np.concatenate((training_feature_set_list, features_train), axis=0)
        validation_feature_set_list = np.concatenate((validation_feature_set_list, features_validation), axis=0)
        testing_feature_set_list = np.concatenate((testing_feature_set_list, features_testing), axis=0)

        training_label_set_list = np.concatenate((training_label_set_list, labels_train), axis=0)
        validation_label_set_list = np.concatenate((validation_label_set_list, labels_validation), axis=0)
        testing_label_set_list = np.concatenate((testing_label_set_list, labels_testing), axis=0)

        training_groundTruth_set_list = np.concatenate((training_groundTruth_set_list, labels_x_train), axis=0)
        validation_groundTruth_set_list = np.concatenate((validation_groundTruth_set_list, labels_x_validation), axis=0)
        testing_groundTruth_set_list = np.concatenate((testing_groundTruth_set_list, labels_x_testing), axis=0)

        # print(training_feature_set_list.shape)

    if interval == 1:
        pass


    elif interval > 1:
        # print(training_feature_set_list.shape)
        training_feature_set_list = training_feature_set_list[::interval]
        validation_feature_set_list = validation_feature_set_list[::interval]
        testing_feature_set_list = testing_feature_set_list[::interval]

        training_label_set_list = training_label_set_list[::interval]
        validation_label_set_list = validation_label_set_list[::interval]
        testing_label_set_list = testing_label_set_list[::interval]

        training_groundTruth_set_list = training_groundTruth_set_list[::interval]
        validation_groundTruth_set_list = validation_groundTruth_set_list[::interval]
        testing_groundTruth_set_list = testing_groundTruth_set_list[::interval]

    else:
        Exception("label_width should be greater or eual than 1")

    return training_feature_set_list, validation_feature_set_list, testing_feature_set_list, training_label_set_list, validation_label_set_list, testing_label_set_list, training_groundTruth_set_list, validation_groundTruth_set_list, testing_groundTruth_set_list


def customized_tanh(x, amp=2.4):
    import tensorflow as tf
    return tf.keras.backend.tanh(x) * amp


def array_1D_push_back(arr, val):
    # append the -1(last) value and delete the 0(1st) value.
    time_len = arr.shape[1]
    feature_len = arr.shape[2]

    arr = arr.reshape(time_len)
    arr = np.delete(arr, 0)
    arr = np.append(arr, val)
    arr = arr.reshape(1, time_len, feature_len)

    return arr


def array_push_back(arr, vals):
    # vals should be a np.array
    # warning: O(n)
    time_len = arr.shape[1]
    feature_len = arr.shape[2]

    arr = arr.reshape(time_len, feature_len)
    arr = np.delete(arr, 0, 0)  # 0th axis and 0th element
    vals = vals.reshape(1, feature_len)
    arr = np.append(arr, vals, axis=0)
    arr = arr.reshape(1, time_len, feature_len)

    return arr