import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.widgets import Slider, Button, RadioButtons
from read_bag import create_LSTM_model, create_dense_model, \
    joint_results, customized_tanh, load_all_experiments, load_bag_files
from LSTM_function import create_LSTM_dataset, create_1D_LSTM_dataset, create_LSTM_MM_dataset
from scipy.ndimage import gaussian_filter1d


# def customized_tanh(x, amp=4, offset=0):
#     return tf.keras.backend.tanh(x) * amp + offset

# This function is for testing purpose!
def quick_arr_predict(arr, model):
    arr = np.array(arr).reshape(1, model.input_shape[1], model.input_shape[2])
    return model.predict(arr)


def rmse(prediction, ground_truth):
    # input should be numpy array
    return np.sqrt(np.mean((prediction - ground_truth) ** 2))


def mae(arry1, arry2):
    # arry1 and arry2 should be numpy array
    return np.mean(np.abs(arry1 - arry2))


def lin_reg(data_array):
    # data_array has a shape [batches, time_stamps, features]
    data_array_x, data_array_y = np.transpose(data_array)
    m, b = np.polyfit(data_array_x, data_array_y, deg=1)
    return b, m, data_array_x


def lin_reg_m(data_array):
    # data_array has a shape [batches, time_stamps, features]
    data_array_x, data_array_y = np.transpose(data_array)
    m, b = np.polyfit(data_array_x, data_array_y, deg=1)
    return m


def relu_cap(x):
    y = np.copy(x)
    for i in range(len(y)):
        if y[i] >= 0:
            y[i] = 0
        elif y[i] <= -2:
            y[i] = -2
        else:
            pass
    return y


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


if __name__ == "__main__":
    # model_weight_h5 = 'LSTM_training_dataset_05102022_MM_output_cell_64_width_8_t_4_old.h5'
    model_weight_h5 = 'LSTM_training_dataset_28102022_MM_output_cell_32_width_12_t_4.h5'
    model = load_model('./LSTM_training/LSTM_models_h5/' + model_weight_h5, custom_objects={"customized_tanh": customized_tanh})
    model.summary()

    # file_folder = '/home/cflai/catkin_ws_py/bag_file/VS_exp/'
    file_folder = '/home/cflai/catkin_ws_py/bag_file/VS_exp/x_axis_28102022/'
    file_dir_training, file_dir_validation = load_bag_files(file_folder)
    exp_results = load_all_experiments(file_dir_training, file_folder + 'training/', plot=False)
    exp_results_validation = load_all_experiments(file_dir_validation, file_folder + 'validation/', plot=False)
    encoder_norm, target_x_norm, target_y_norm = joint_results(exp_results)
    encoder_norm_validation, target_x_norm_validation, target_y_norm_validation = joint_results(exp_results_validation)

    width = model.input_shape[1]  # use the previous training feature width
    feature_dim = model.input_shape[2]
    output_dim = model.output_shape[1]

    # features, labels, labels_x = create_1D_LSTM_dataset(target_x_norm,
    #                                                     encoder_norm,
    #                                                     feature_width=width
    #                                                     )
    if feature_dim == 1 and output_dim == 1:
        features, labels, labels_x = create_1D_LSTM_dataset(target_x_norm_validation,
                                                            encoder_norm_validation,
                                                            feature_width=width
                                                            )

    elif feature_dim == 2 and output_dim == 1:
        features, labels, labels_x = create_LSTM_dataset(target_x_norm_validation,
                                                         encoder_norm_validation,
                                                         feature_width=width
                                                         )
    elif model_weight_h5.split('_')[4] == 'MM' and output_dim >= 2:
        features, labels, labels_x = create_LSTM_MM_dataset(encoder_norm, target_x_norm,
                                                            feature_width=width,
                                                            label_width=output_dim)
        print('test_MM_SUCCCESS')
    else:
        print(model_weight_h5.split('_')[4])
        raise Exception('feature_dim not defined yet')

    prediction_LSTM = model.predict(features)
    # print('all features shape', features.shape, '\none feature shape:', features[0:2].shape)
    # print('two features', features[0:2])
    # print('one prediction', model.predict(features[0]))
    features_m_array = np.array(list(map(lin_reg_m, features)))
    labels_m_array = np.array(list(map(lin_reg_m, labels)))
    prediction_LSTM_m_array = np.array(list(map(lin_reg_m, prediction_LSTM)))

    if model_weight_h5.split('_')[4] == 'MM':
        fig, axs = plt.subplots(3, 1)
        n = 200
        pre = np.transpose(features[n])  # previous
        fut = np.transpose(prediction_LSTM[n])
        gt = np.transpose(labels[n])
        data_encoder_gt = features[:, 0, 0]
        data_vs_gt = features[:, 0, 1]
        data_encoder_pred = prediction_LSTM[:, :, 0]
        data_vs_pred = prediction_LSTM[:, :, 1]
        data_encoder_label = labels[:, :, 0]
        data_vs_label = labels[:, :, 1]
        # axs[0]
        [line] = axs[0].plot(pre[0], pre[1], color='orange', marker='o', label='previous_time')
        [line2] = axs[0].plot(fut[0], fut[1], color='blue', marker='x', label='prediction_future_time')
        [line3] = axs[0].plot(gt[0], gt[1], color='green', marker='^', label='truth_future_time')
        feature_b, feature_m, feature_x = lin_reg(features[n])
        prediction_LSTM_b, prediction_LSTM_m, prediction_LSTM_x = lin_reg(prediction_LSTM[n])
        labels_b, labels_m, labels_x = lin_reg(labels[n])
        [line4] = axs[0].plot(feature_x, feature_b + feature_m * feature_x, '-')
        [line5] = axs[0].plot(prediction_LSTM_x, prediction_LSTM_b + prediction_LSTM_m * prediction_LSTM_x, '-')
        [line6] = axs[0].plot(labels_x, labels_b + labels_m * labels_x, '-')
        txt = axs[0].text(features[n, -1, 0] - 0.2, features[n, -1, 1] + 0.2, "errors", size=10, ha="left", color="b")
        axs[0].legend(loc='upper right')

        # axs[1]
        [line7] = axs[1].plot(range(len(features_m_array)), features_m_array, color='orange', label='J_history')
        [line8] = axs[1].plot(range(len(labels_m_array)), labels_m_array, color='green', label='J_real_future')
        [line9] = axs[1].plot(range(len(prediction_LSTM_m_array)), prediction_LSTM_m_array, color='blue',
                              label='J_pred_future')
        [line10] = axs[1].plot(0, features_m_array[0], 'rx', label='cursors')

        filtered_prediction_array = np.tanh(prediction_LSTM_m_array + 1.3)
        [line11] = axs[1].plot(range(len(filtered_prediction_array)), filtered_prediction_array - 1,
                               label='J_pred_future_filtered')
        txt_2 = axs[1].text(5, 5, "J_inverse_of_prediction", size=10, ha="left", color="b")
        axs[1].legend(loc='upper right')
        # axs[2]
        [line12] = axs[2].plot(data_encoder_gt, label='motor angle (normalized)')
        [line13] = axs[2].plot(data_vs_gt, label='visual target (normalized)')
        axs[2].legend(loc='upper right')

        range_slider_axs = fig.add_axes([0.25, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        range_slider = Slider(range_slider_axs, 'range', 200, 600, valinit=n, orientation='horizontal')


        def sliders_on_changed(val):
            # datasets results
            pre = np.transpose(features[int(range_slider.val)])
            fut = np.transpose(prediction_LSTM[int(range_slider.val)])
            gt = np.transpose(labels[int(range_slider.val)])
            line.set_xdata(pre[0])
            line.set_ydata(pre[1])
            line2.set_xdata(fut[0])
            line2.set_ydata(fut[1])
            line3.set_xdata(gt[0])
            line3.set_ydata(gt[1])

            # linear regression
            feature_b, feature_m, feature_x = lin_reg(features[int(range_slider.val)])
            prediction_LSTM_b, prediction_LSTM_m, prediction_LSTM_x = lin_reg(prediction_LSTM[int(range_slider.val)])
            labels_b, labels_m, labels_x = lin_reg(labels[int(range_slider.val)])
            line4.set_xdata(feature_x)
            line4.set_ydata(feature_m * feature_x + feature_b)
            line5.set_xdata(prediction_LSTM_x)
            line5.set_ydata(prediction_LSTM_m * prediction_LSTM_x + prediction_LSTM_b)
            line6.set_xdata(labels_x)
            line6.set_ydata(labels_m * labels_x + labels_b)

            axs[0].set_xlim(np.array([-0.3 + features[int(range_slider.val), -1, 0],
                                      0.3 + features[int(range_slider.val), -1, 0]]))
            axs[0].set_ylim(np.array([-0.3 + features[int(range_slider.val), -1, 1],
                                      0.3 + features[int(range_slider.val), -1, 1]]))

            txt.set_position((features[int(range_slider.val), -1, 0] - 0.29,
                              features[int(range_slider.val), -1, 1] + 0.18))
            print_text = 'error_prediction: \t' + str(round(prediction_LSTM_m - labels_m, 2)) + '\n' \
                         + 'error_history: \t' + str(round(feature_m - labels_m, 2))
            txt.set_text(print_text)

            # axs[1] figure:
            line7.set_xdata(range(int(range_slider.val) - 50, int(range_slider.val) + 50))
            line7.set_ydata(features_m_array[int(range_slider.val) - 50:int(range_slider.val) + 50])
            line8.set_xdata(range(int(range_slider.val) - 50, int(range_slider.val) + 50))
            line8.set_ydata(labels_m_array[int(range_slider.val) - 50:int(range_slider.val) + 50])
            line9.set_xdata(range(int(range_slider.val) - 50, int(range_slider.val) + 50))
            line9.set_ydata(prediction_LSTM_m_array[int(range_slider.val) - 50:int(range_slider.val) + 50])
            line10.set_xdata(int(range_slider.val))
            line10.set_ydata(prediction_LSTM_m_array[int(range_slider.val)])
            line11.set_xdata(range(int(range_slider.val) - 50, int(range_slider.val) + 50))
            line11.set_ydata(filtered_prediction_array[int(range_slider.val) - 50:int(range_slider.val) + 50] - 1)

            axs[1].set_xlim((int(range_slider.val) - 50, int(range_slider.val) + 50))
            txt_2.set_position((int(range_slider.val) - 38, 8))
            print_text_2 = 'J_inverse_of_prediction: \n' + str(round(prediction_LSTM_m, 2))
            txt_2.set_text(print_text_2)

            # axs[2] figure:
            line12.set_xdata(range(int(range_slider.val) - 50, int(range_slider.val) + 50))
            line12.set_ydata(data_encoder_gt[int(range_slider.val) - 50:int(range_slider.val) + 50])
            line13.set_xdata(range(int(range_slider.val) - 50, int(range_slider.val) + 50))
            line13.set_ydata(data_vs_gt[int(range_slider.val) - 50:int(range_slider.val) + 50])
            axs[2].set_xlim((int(range_slider.val) - 50, int(range_slider.val) + 50))

            fig.canvas.draw_idle()


        range_slider.on_changed(sliders_on_changed)

        axs[0].set_xlim(np.array([-0.3 + features[n, -1, 0],
                                  0.3 + features[n, -1, 0]]))
        axs[0].set_ylim(np.array([-0.3 + features[n, -1, 1],
                                  0.3 + features[n, -1, 1]]))

        axs[0].set_xlabel('q')
        axs[0].set_ylabel('cv')
        axs[1].set_xlabel('index')
        axs[1].set_ylabel('J (cv/q)')
        axs[2].set_xlabel('time index')
        axs[2].set_ylabel('visual target or motor angle')

        fig.suptitle(model_weight_h5[:-3].split('_', maxsplit=4)[-1])

        plt.legend()
        plt.show()

    else:
        fig, axs = plt.subplots(1, 2)

        a = 200
        b = 400

        [line3] = axs[0].plot(range(len(np.squeeze(prediction_LSTM[a:b]))), np.squeeze(prediction_LSTM[a:b]),
                              marker='x')
        # ax.scatter(exp_results[0].time_stamp[5:], np.squeeze(prediction_Dense), marker='^')
        [line4] = axs[0].plot(range(len(np.squeeze(labels[a:b]))), np.squeeze(labels[a:b]), marker='o')
        # axs[1].plot(encoder_norm)
        # axs[1].plot(target_x_norm)
        # axs[1].plot(exp_results[0].encoders)
        # axs[1].plot(exp_results[0].target_x)
        # axs[1].plot(exp_results[0].vel_array_sync)

        [line] = axs[1].plot(np.squeeze(prediction_LSTM)[a:b], np.squeeze(labels_x)[a:b], marker='x',
                             label='prediction')
        [line2] = axs[1].plot(np.squeeze(labels)[a:b], np.squeeze(labels_x)[a:b], marker='o', label='raw')
        axs[0].set_ylim([-3, 3])
        axs[1].set_xlim([-3, 3])
        axs[1].set_ylim([-3, 3])
        range_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        range_slider = Slider(range_slider_ax, 'range', 0, 5000, valinit=a)
        range_slider_ax_2 = fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        range_slider_2 = Slider(range_slider_ax_2, 'range', 0, 5000, valinit=b)
        print('RMSE:', rmse(prediction_LSTM, labels))
        model.evaluate(features, labels, verbose=2)


        def sliders_on_changed(val):
            line.set_xdata(np.squeeze(prediction_LSTM)[int(range_slider.val): int(range_slider_2.val)])
            line.set_ydata(np.squeeze(labels_x)[int(range_slider.val): int(range_slider_2.val)])
            line2.set_xdata(np.squeeze(labels)[int(range_slider.val): int(range_slider_2.val)])
            line2.set_ydata(np.squeeze(labels_x)[int(range_slider.val): int(range_slider_2.val)])

            line3.set_ydata(np.squeeze(prediction_LSTM)[int(range_slider.val): int(range_slider_2.val)])
            line3.set_xdata(range(len(np.squeeze(prediction_LSTM[int(range_slider.val): int(range_slider_2.val)]))))
            line4.set_ydata(np.squeeze(labels)[int(range_slider.val): int(range_slider_2.val)])
            line4.set_xdata(range(len(np.squeeze(labels[int(range_slider.val): int(range_slider_2.val)]))))
            fig.canvas.draw_idle()


        range_slider.on_changed(sliders_on_changed)
        range_slider_2.on_changed(sliders_on_changed)

        # ax.plot(np.squeeze(labels_x), np.squeeze(prediction_LSTM), marker='x', label='prediction')
        # ax.scatter(np.squeeze(labels_x), np.squeeze(labels), marker='o', label='raw')
        axs[0].set_xlabel('data point')
        axs[0].set_ylabel('q (encoders) prediction')
        axs[1].set_ylabel('cv (pixel)')
        axs[1].set_xlabel('q (encoders)')

        plt.legend()
        plt.show()


    def filter_visualization():
        m = 1
        fig2, axs2 = plt.subplots(3, 1)
        data_gt_1 = np.array(labels_m_array[830:1040])
        data_1 = np.array(prediction_LSTM_m_array[830:1040])
        data_gt_2 = np.array(labels_m_array[1560:1790])
        data_2 = np.array(prediction_LSTM_m_array[1560:1790])
        data_gt_3 = np.array(labels_m_array[250:470])
        data_3 = np.array(prediction_LSTM_m_array[250:470])

        # filtered
        data_1_filtered = np.tanh(data_1 + m)
        data_2_filtered = np.tanh(data_2 + m)
        data_3_filtered = np.tanh(data_3 + m)

        axs2[0].plot(range(len(data_1)), data_1, label='prediction line')
        axs2[0].plot(range(len(data_gt_1)), data_gt_1, label='ground truth line')
        axs2[0].plot(range(len(data_1_filtered)), data_1_filtered, label='filtered line')

        axs2[1].plot(range(len(data_2)), data_2, label='prediction line')
        axs2[1].plot(range(len(data_gt_2)), data_gt_2 + m, label='ground truth line')
        axs2[1].plot(range(len(data_2_filtered)), data_2_filtered, label='filtered line')

        axs2[2].plot(range(len(data_3)), data_3, label='prediction line')
        axs2[2].plot(range(len(data_gt_3)), data_gt_3 + m, label='ground truth line')
        axs2[2].plot(range(len(data_3_filtered)), data_3_filtered, label='filtered line')

        axs2[0].legend(loc='upper right')
        axs2[1].legend(loc='upper right')
        axs2[2].legend(loc='upper right')
        axs2[0].set_ylabel('J(q/cv)')
        axs2[1].set_ylabel('J(q/cv)')
        axs2[2].set_ylabel('J(q/cv)')
        axs2[2].set_xlabel('index')

        plt.legend()
        plt.show()

        return


    def filter_comparison():
        m = 1
        fig3, axs3 = plt.subplots(1, 1)
        [line_axs3_1] = axs3.plot(range(len(features_m_array)), features_m_array, label='GT line')
        # define all the 4 lines to compare:
        ## 1. original
        [line_axs3_2] = axs3.plot(range(len(gaussian_filter1d(prediction_LSTM_m_array, sigma=1))),
                                  gaussian_filter1d(prediction_LSTM_m_array, sigma=1), label='prediction line')
        ## 2. tanh
        p_filtered_tanh = np.tanh(prediction_LSTM_m_array + m) - 1
        [line_axs3_3] = axs3.plot(range(len(p_filtered_tanh)), p_filtered_tanh, label='tanh line')
        ## 3. sigmoid
        p_filtered_sigmoid = sigmoid(prediction_LSTM_m_array + 1.5) * 2 - 2
        [line_axs3_4] = axs3.plot(range(len(p_filtered_sigmoid)), p_filtered_sigmoid, label='sigmoid line')
        ## 4. relu_cap
        p_filtered_reLu = relu_cap(prediction_LSTM_m_array)
        [line_axs3_5] = axs3.plot(range(len(p_filtered_reLu)), p_filtered_reLu, label='reLu line')

        range_slider_window_size_ax3 = fig3.add_axes([0.25, 0.04, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        range_slider_window_size = Slider(range_slider_window_size_ax3, 'window size', 300, 500, valinit=50)
        range_slider_midpoint_ax3 = fig3.add_axes([0.25, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        range_slider_midpoint = Slider(range_slider_midpoint_ax3, 'midpoint', 500, 1000, valinit=100)

        txt_errors = axs3.text(features[n, -1, 0] - 0.2, features[n, -1, 1] + 0.2,
                               str(mae(features_m_array, prediction_LSTM_m_array)), size=10, ha="left", color="b")

        def sliders_on_changed_axs3(val):
            midpoint = int(range_slider_midpoint.val)
            window_size = int(range_slider_window_size.val)
            window_boundary = (midpoint - window_size, midpoint + window_size)
            window_range = range(window_boundary[0], window_boundary[1])
            line_axs3_1.set_xdata(window_range)
            line_axs3_1.set_ydata(features_m_array[window_range])
            line_axs3_2.set_xdata(window_range)
            line_axs3_2.set_ydata(prediction_LSTM_m_array[window_range])
            line_axs3_3.set_xdata(window_range)
            line_axs3_3.set_ydata(p_filtered_tanh[window_range])
            line_axs3_4.set_xdata(window_range)
            line_axs3_4.set_ydata(p_filtered_sigmoid[window_range])
            line_axs3_5.set_xdata(window_range)
            line_axs3_5.set_ydata(p_filtered_reLu[window_range])

            axs3.set_xlim(window_boundary)
            axs3.set_ylim(3, -3)

            # txt_errors.set_position((int(range_slider_midpoint.val) - 38, 2))
            # print_text_3 = 'GT overall Mean absolute error: \n' + \
            #                'GT vs. original' + str(
            #     round(mae(features_m_array[window_range], prediction_LSTM_m_array[window_range]), 2)) + '\n' + \
            #                'GT vs. tanh' + str(
            #     round(mae(features_m_array[window_range], p_filtered_tanh[window_range]), 2)) + '\n' + \
            #                'GT vs. sigmoid' + str(
            #     round(mae(features_m_array[window_range], p_filtered_sigmoid[window_range]), 2)) + '\n' + \
            #                'GT vs. reLu:' + str(
            #     round(mae(features_m_array[window_range], p_filtered_reLu[window_range]), 2))
            #
            # txt_errors.set_text(print_text_3)
            fig.canvas.draw_idle()

        range_slider_window_size.on_changed(sliders_on_changed_axs3)
        range_slider_midpoint.on_changed(sliders_on_changed_axs3)

        print('GT overall Mean absolute error:')
        print(model_weight_h5.split('_')[4:])
        print('vs. original:', mae(features_m_array, prediction_LSTM_m_array))
        print('vs. tanh:', mae(features_m_array, p_filtered_tanh))
        print('vs. sigmoid:', mae(features_m_array, p_filtered_sigmoid))
        print('vs. reLu:', mae(features_m_array, p_filtered_reLu))
        axs3.legend(loc='upper right')
        axs3.set_xlabel('index in time')
        axs3.set_ylabel('J (cv/q)')
        plt.legend()

        return


    def result_visualization(init=0, end=-1, interval=4, k=0):
        fig4, axs4 = plt.subplots(2, 3, figsize=(14, 9))
        marker_size = 15
        data_encoder_gt = features[init:end:interval, 0, 0]
        data_vs_gt = features[init:end:interval, 0, 1]
        data_encoder_pred = prediction_LSTM[init:end:interval, :, 0]
        data_vs_pred = prediction_LSTM[init:end:interval, :, 1]
        data_encoder_label = labels[init:end:interval, :, 0]
        data_vs_label = labels[init:end:interval, :, 1]

        rmse_encoder = rmse(data_encoder_pred[:, k], data_encoder_label[:, k])
        mae_encoder = mae(data_encoder_pred[:, k], data_encoder_label[:, k])
        rmse_vs = rmse(data_vs_pred[:, k], data_vs_label[:, k])
        mae_vs = mae(data_vs_pred[:, k], data_vs_label[:, k])
        ###############first figure#################
        axs4[0][0].plot(data_encoder_gt, data_vs_gt, '-o', label='ground truth')
        axs4[0][0].set_title('hysteresis - visual target vs motor angle')
        axs4[0][1].plot(data_encoder_label[:, 0], data_vs_label[:, 0], '-o', label='1-step future')
        axs4[0][1].plot(data_encoder_pred[:, 0], data_vs_pred[:, 0], 'x', label='LSTM prediction')
        axs4[0][1].set_title('ground truth and prediction in 1-step')
        axs4[0][2].plot(data_encoder_label[:, 3], data_vs_label[:, 3], '-o', label='4-step future')
        axs4[0][2].plot(data_encoder_pred[:, 3], data_vs_pred[:, 3], 'x', label='LSTM prediction')
        axs4[0][2].set_title('ground truth and prediction in 4-step')
        axs4[1][0].scatter(range(len(data_vs_label[:, 0])), data_vs_label[:, 0],
                           s=marker_size, label='visual target', color='g', marker='o')
        axs4[1][0].scatter(range(len(data_encoder_label[:, 0])), data_encoder_label[:, 0],
                           s=marker_size, label='motor angle', color='b', marker='o')
        axs4[1][0].set_title('motor angle and visual targets')
        axs4[1][1].scatter(range(len(data_encoder_label[:, 0])), data_encoder_label[:, 0],
                           s=marker_size, label='motor angle', color='b', marker='o')
        axs4[1][1].scatter(range(len(data_encoder_pred[:, 0])), data_encoder_pred[:, 0],
                           s=marker_size, label='motor angle - prediction', color='r', marker='x')
        axs4[1][1].set_title('motor angle: truth vs prediction')
        axs4[1][2].scatter(range(len(data_vs_label[:, 0])), data_vs_label[:, 0],
                           s=marker_size, label='visual target', color='g', marker='o')
        axs4[1][2].scatter(range(len(data_vs_pred[:, 0])), data_vs_pred[:, 0],
                           s=marker_size, label='visual target - prediction', color='r', marker='x')
        axs4[1][2].set_title('visual targets: truth vs prediction')
        fig4.suptitle('LSTM model - Varying amplitude')
        for i in range(2):
            for j in range(3):
                if i == 0:
                    axs4[i][j].legend(loc='upper right')
                    axs4[i][j].set_xlabel('q (normalized theta)')
                elif i == 1:
                    axs4[i][j].legend(loc='upper left')
                    axs4[i][j].set_ylim(-2, 2.3)
                    axs4[i][j].set_xlabel('time (seconds)')

        axs4[0][0].set_ylabel('cv (normalized pixel)')
        axs4[1][0].set_ylabel('cv (in green); q (in blue)')
        axs4[1][1].set_ylabel('q')
        axs4[1][2].set_ylabel('cv')
        ############### second figure #################
        fig5, axs5 = plt.subplots(2, 4, figsize=(14, 9))
        marker_size = 15
        # motor angle
        axs5[0][0].scatter(range(len(data_encoder_pred[:, 0])), data_encoder_pred[:, 0],
                           s=marker_size, label='motor angle - prediction', color='r', marker='x')
        axs5[0][0].scatter(range(len(data_encoder_label[:, 0])), data_encoder_label[:, 0],
                           s=marker_size, label='motor angle', color='b', marker='o')
        axs5[0][0].set_title('motor angle, 1-step future')
        axs5[0][1].scatter(range(len(data_encoder_pred[:, 1])), data_encoder_pred[:, 1],
                           s=marker_size, label='motor angle - prediction', color='r', marker='x')
        axs5[0][1].scatter(range(len(data_encoder_label[:, 1])), data_encoder_label[:, 1],
                           s=marker_size, label='motor angle', color='b', marker='o')
        axs5[0][1].set_title('motor angle, 2-step future')
        axs5[0][2].scatter(range(len(data_encoder_pred[:, 2])), data_encoder_pred[:, 2],
                           s=marker_size, label='motor angle - prediction', color='r', marker='x')
        axs5[0][2].scatter(range(len(data_encoder_label[:, 2])), data_encoder_label[:, 2],
                           s=marker_size, label='motor angle', color='b', marker='o')
        axs5[0][2].set_title('motor angle, 3-step future')
        axs5[0][3].scatter(range(len(data_encoder_pred[:, 3])), data_encoder_pred[:, 3],
                           s=marker_size, label='motor angle - prediction', color='r', marker='x')
        axs5[0][3].scatter(range(len(data_encoder_label[:, 3])), data_encoder_label[:, 3],
                           s=marker_size, label='motor angle', color='b', marker='o')
        axs5[0][3].set_title('motor angle, 4-step future')
        # VS
        axs5[1][0].scatter(range(len(data_vs_label[:, 0])), data_vs_label[:, 0],
                           s=marker_size, label='visual target', color='g', marker='o')
        axs5[1][0].scatter(range(len(data_vs_pred[:, 0])), data_vs_pred[:, 0],
                           s=marker_size, label='visual target - prediction', color='r', marker='x')
        axs5[1][0].set_title('visual targets: 1-step future')
        axs5[1][1].scatter(range(len(data_vs_label[:, 1])), data_vs_label[:, 1],
                           s=marker_size, label='visual target', color='g', marker='o')
        axs5[1][1].scatter(range(len(data_vs_pred[:, 1])), data_vs_pred[:, 1],
                           s=marker_size, label='visual target - prediction', color='r', marker='x')
        axs5[1][1].set_title('visual targets: 2-step future')
        axs5[1][2].scatter(range(len(data_vs_label[:, 2])), data_vs_label[:, 2],
                           s=marker_size, label='visual target', color='g', marker='o')
        axs5[1][2].scatter(range(len(data_vs_pred[:, 2])), data_vs_pred[:, 2],
                           s=marker_size, label='visual target - prediction', color='r', marker='x')
        axs5[1][2].set_title('visual targets: 3-step future')
        axs5[1][3].scatter(range(len(data_vs_label[:, 3])), data_vs_label[:, 3],
                           s=marker_size, label='visual target', color='g', marker='o')
        axs5[1][3].scatter(range(len(data_vs_pred[:, 3])), data_vs_pred[:, 3],
                           s=marker_size, label='visual target - prediction', color='r', marker='x')
        axs5[1][3].set_title('visual targets: 4-step future')

        fig5.suptitle('LSTM model - Varying time steps')
        for i in range(2):
            for j in range(4):
                axs5[i][j].set_xlabel('time (seconds)')
                if i == 0:
                    axs5[i][j].legend(loc='upper right')
                    axs5[i][j].set_ylim(-2, 2.3)
                elif i == 1:
                    axs5[i][j].legend(loc='upper left')
                    axs5[i][j].set_ylim(-2, 2.3)

        axs5[0][0].set_ylabel('q (normalized motor)')
        axs5[0][1].set_ylabel('cv (normalized pixel)')

        plt.legend()
        plt.show()

        return rmse_encoder, mae_encoder, rmse_vs, mae_vs


    result_visualization(init=862, end=1710, k=0)
    filter_visualization()
    filter_comparison()
