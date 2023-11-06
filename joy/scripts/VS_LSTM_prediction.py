#!/usr/bin/env python3

######################################################

# This script is the LSTM network for prediction the future trajectories.

# sub topic: rospy_tutorials.msg/Floats: /motors_states, /target_centroid
# sub topic: std_msgs.msg/Float64: /p_error
# pub topic: std_msgs.msg/Float64: /predicted_jacobian_value

# LSTM_model_24_08_1D_128_inverse.h5
# encoder_mean 37.29185981828296 encoder_std 429.76998764382176
# x_mean 135.09153743738946 x_std 55.697075747868375
# y_mean 155.26704438993093 y_std 9.390104924529114

# new_input_LSTM_dataset_05102022_64.h5
# encoder_mean 241.57176470588234 encoder_std 175.47470959645005
# x_mean 127.13583277613233 x_std 26.987402675971836
# y_mean 125.24811772435594 y_std 1.7555774364242558

######################################################
import os
import rospy
from std_msgs.msg import Float64
from rospy_tutorials.msg import Floats
from read_bag import customized_tanh
from tensorflow.keras.models import load_model
from numpy import zeros as npzeros
from numpy import array as nparray
from numpy import arange as nparange
from numpy import concatenate as npconcatenate
from LSTM_function import array_1D_push_back

print(os.getcwd())
# initialize
global target_error, pub2, pub3
actual_target_pos_CV_norm = 125.0
target_error = 0.0
motors_states_norm = 0.0
model = load_model('/home/cflai/catkin_ws_py/src/joy/scripts/new_input_LSTM_dataset_05102022_64.h5',
                   custom_objects={"customized_tanh": customized_tanh})
historical_feature_CV_norm = npzeros((1, model.input_shape[1], 1))
historical_feature_joint = npzeros((1, model.input_shape[1], 1))


def test_function_store_arr(arr):
    arr_len = arr.shape[1]
    arr = arr.reshape(arr_len)
    print(arr.shape)
    return arr


def callback_error(msg):
    global target_error
    kp = 1
    target_error = msg.data / kp


def callback_motor_states(data):
    global motors_states_norm
    motors_states_norm = norm_val(data.data[0], mean=241.57, std=175.47)


def callback_actual_target_sync(data):
    global actual_target_pos_CV_norm, joint_cv_syn, historical_feature_CV_norm, historical_feature_joint
    cv_norm = norm_val(data.data[0], mean=127.14, std=26.99)
    historical_feature_CV_norm = array_1D_push_back(historical_feature_CV_norm, cv_norm)
    historical_feature_joint = array_1D_push_back(historical_feature_joint, data.data[0])  # 1D
    actual_target_pos_CV_norm = cv_norm
    joint_cv_syn = [motors_states_norm, actual_target_pos_CV_norm]


def LSTM_node():
    global pub2, pub3
    function_selection = 'two_features'  # 'one_feature', 'two_features', 'two_features_two_predictions'
    rospy.init_node('LSTM_prediction', anonymous=True)
    pub = rospy.Publisher('/predicted_jacobian_value', Float64, queue_size=2)
    pub2 = rospy.Publisher('/norm_val', Floats, queue_size=1)
    pub3 = rospy.Publisher('testing_array', Floats, queue_size=1)
    rospy.Subscriber("/p_error", Float64, callback_error)
    rospy.Subscriber("/motors_states", Floats, callback_motor_states)
    rospy.Subscriber("/target_centroid", Floats, callback_actual_target_sync)
    r = rospy.Rate(20)  # Hz 128:max25HZ
    jacobian_value = Float64()
    jacobian_value.data = 0.0  # should initialize jacobian number

    while not rospy.is_shutdown():
        if function_selection == 'one_feature':
            jacobian_value.data = calculate_J_one_feature(historical_feature_CV_norm)
        elif function_selection == 'two_features':
            jacobian_value.data = calculate_J_one_feature_multi_future(historical_feature_CV_norm)
        pub.publish(jacobian_value)
        # rospy.loginfo(rospy.get_caller_id() + "  prediction value: %s",
        #               jacobian_value.data)
        r.sleep()
        # print(historical_feature_joint)
    return


def calculate_J_one_feature(historical_feature_CV_norm, step=0.008):
    norm_array = Floats()
    norm_array.data = [0, 0, 0, 0, 0]
    testing_array = Floats()
    target_error_norm = norm_val(target_error, mean=0.0, std=26.99)  # ? mean should be zero or??
    desired_cv_feature_norm = actual_target_pos_CV_norm + (target_error_norm * step)  # + vs -??
    # I am guessing that I may need a fileter here... ?
    new_feature_norm = array_1D_push_back(historical_feature_CV_norm, desired_cv_feature_norm)
    # testing function:
    testing_array.data = test_function_store_arr(new_feature_norm)

    # save all the value and the prediction
    cv_old = actual_target_pos_CV_norm
    cv_new = desired_cv_feature_norm
    q_old = motors_states_norm
    # to be done: normalization of te prediction
    q_new = model.predict(new_feature_norm)
    print("predict val:", q_new, "previous vals:",
          new_feature_norm[0][-9],
          new_feature_norm[0][-8],
          new_feature_norm[0][-7],
          new_feature_norm[0][-6],
          new_feature_norm[0][-5],
          new_feature_norm[0][-4],
          new_feature_norm[0][-3],
          new_feature_norm[0][-2],
          new_feature_norm[0][-1]
          )


          # print('the value:', desired_cv_feature_norm)
    j = (cv_new - cv_old) / (q_new - q_old)
    # print('feature_array_start:', new_feature_norm[0][0:5], 'feature_array_end:', new_feature_norm[0][-5:])
    # print('the value: {0:.3f}, {1:.3f}, {2:.3f}, {3:.3f}, {4:.3f}, {5:.3f}'.format(
    #     cv_new, cv_old, q_new[0][0], q_old, j[0][0], target_error_norm))
    norm_array.data = [cv_new, cv_old, q_new[0][0], q_old, j]
    pub2.publish(norm_array)
    pub3.publish(testing_array)

    return j


def calculate_J_one_feature_multi_future(historical_feature_CV_norm, step=0.008, steps=3.0):
    norm_array = Floats()
    # norm_array.data = [0, 0, 0, 0, 0]
    target_error_norm = norm_val(target_error, mean=0.0, std=26.99)
    steps = nparange(steps) + 1.0
    desired_cv_feature_norm_list = actual_target_pos_CV_norm + (target_error_norm * step * steps)  # + vs -??
    flag = 0
    for val in desired_cv_feature_norm_list:
        if flag == 0:
            new_feature_norm = array_1D_push_back(historical_feature_CV_norm, val)
            new_feature_norm_list = new_feature_norm
            flag = 1
        else:
            new_feature_norm = array_1D_push_back(historical_feature_CV_norm, val)
            new_feature_norm_list = npconcatenate((new_feature_norm_list, new_feature_norm), axis=0)


    # save all the value and the prediction
    cv_old = actual_target_pos_CV_norm
    cv_new = desired_cv_feature_norm_list
    q_old = motors_states_norm
    q_new = model.predict(new_feature_norm_list)
    j = (cv_new[0] - cv_old) / (q_new[0][0] - q_old)
    # print('cv_new', desired_cv_feature_norm_list, 'q_new', q_new)
    # we need a new way to determine J if necessary
    # print(type(cv_old), type(cv_new), type(q_old), type(q_new))
    cv_old = [cv_old]
    cv_new = cv_new.tolist()
    q_old = [q_old]
    q_new = q_new
    # print(cv_new[:], cv_old, q_new[:], q_old, j)
    norm_array.data = cv_new[:] + cv_old + q_new[:, 0].tolist() + q_old + [j]
    print(norm_array.data)
    pub2.publish(norm_array)

    # testing function:
    # testing_array = Floats()
    # testing_array.data = test_function_store_arr(new_feature_norm)
    # pub3.publish(testing_array)

    return j


def calculate_J_two_features(historical_feature):
    # save all the value and the prediction
    cv_old = actual_target_pos_CV
    cv_new = desired_cv_feature
    q_old = motors_states_norm
    q_new = model.predict(new_feature)
    print(cv_new, cv_old, q_new, q_old)
    j = (cv_new - cv_old) / (q_new - q_old)

    return j


def norm_val(val, mean, std):
    val = (val - mean) / std
    return val


def create_multi_future_feature(feature_CV_norm, error_norm, steps=1, step=0.008):
    new_feature_array = feature_CV_norm
    cv_future_list = []
    for i in range(steps):
        calculate_cv_feature_norm_one_step = actual_target_pos_CV_norm + (error_norm * step * i)
        new_feature_array = array_1D_push_back(new_feature_array, calculate_cv_feature_norm_one_step)
        cv_future_list.append(calculate_cv_feature_norm_one_step)

    return new_feature_array, nparray(cv_future_list)


if __name__ == '__main__':
    try:
        LSTM_node()
    except:
        pass
