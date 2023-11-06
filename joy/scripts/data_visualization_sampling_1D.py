import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
# from read_bag import load_all_experiments
from bagpy import bagreader
import pandas as pd
from matplotlib.widgets import Slider
import numpy as np

def single_prediction_calculate_J_results(df):

    df.columns = ['Time', 'cv_prediction', 'cv_current', 'q_prediction', 'q_current', 'J_LSTM']

    df['cv_previous'] = df['cv_current'].shift(1)
    df['cv_next'] = df['cv_current'].shift(-1)
    df['q_previous'] = df['q_current'].shift(1)
    df['q_next'] = df['q_current'].shift(-1)
    df['J_SOTA'] = df.apply(lambda x: (x.cv_current-x.cv_previous)/(x.q_current-x.q_previous), axis=1)
    df['J_ground_truth'] = df.apply(lambda x: (x.cv_next - x.cv_current) / (x.q_next - x.q_current), axis=1)
    df['error_SOTA'] = (df['J_ground_truth'] - df['J_SOTA']).abs()
    df['error_LSTM'] = (df['J_ground_truth'] - df['J_LSTM']).abs()

    return df


if __name__ == "__main__":

    fig, axs = plt.subplots(1, 2)

    file_folder = '/home/cflai/catkin_ws_py/bag_file/norm_val/'
    trial_files = [f for f in listdir(file_folder) if isfile(join(file_folder, f))]
    # trial_results = load_all_experiments(file_folder, file_folder + 'validation/')

    for name in trial_files:
        bag_list = []
        b = bagreader(file_folder + name)
        bag_list.append(b)
        print(name)

    norm_val = bag_list[0].message_by_topic('/norm_val')
    df = pd.read_csv(norm_val)
    df = single_prediction_calculate_J_results(df)
    time = df['Time'].tolist()
    cv_prediction = df['cv_prediction'].tolist()[6:]
    cv_current = df['cv_current'].tolist()[6:]
    q_prediction = df['q_prediction'].tolist()[:-6]
    q_current = df['q_current'].tolist()[:-6]

    starting_point = 200
    time_width = 10

    [line] = axs[0].plot(cv_current[starting_point:starting_point + time_width],
                         q_current[starting_point:starting_point + time_width],
                         marker='o', label='ground truth')
    [line2] = axs[0].plot(cv_prediction[starting_point + time_width],
                          q_prediction[starting_point + time_width],
                          marker='x', label='prediction')
    [line3] = axs[0].plot(cv_current[starting_point + time_width],
                          q_current[starting_point + time_width],
                          marker='+', label='prediction')
    [line4] = axs[1].plot(q_current[starting_point:starting_point + time_width],
                          cv_current[starting_point:starting_point + time_width],
                          marker='o', label='ground truth')
    [line5] = axs[1].plot(q_prediction[starting_point + time_width],
                          cv_prediction[starting_point + time_width],
                          marker='x', label='prediction')
    [line6] = axs[1].plot(q_current[starting_point + time_width],
                          cv_current[starting_point + time_width],
                          marker='+', label='prediction')
    x = np.array([-2, -1, 0, 1, 2])
    m = -0.81
    b = 0.024
    axs[1].plot(x, m*x+b, 'r-')
    m, b = np.polyfit(q_current, cv_current, deg=1)

    axs[1].plot(x, m * x + b, 'g-')

    range_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    range_slider = Slider(range_slider_ax, 'range', 0, 500, valinit=starting_point)
    range_slider_ax_2 = fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    range_slider_2 = Slider(range_slider_ax_2, 'range', 0, 500, valinit=time_width)


    def sliders_on_changed(val):
        line.set_xdata(cv_current[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line.set_ydata(q_current[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line2.set_xdata(cv_prediction[int(range_slider.val) + int(range_slider_2.val)])
        line2.set_ydata(q_prediction[int(range_slider.val) + int(range_slider_2.val)])
        line3.set_xdata(cv_current[int(range_slider.val) + int(range_slider_2.val)])
        line3.set_ydata(q_current[int(range_slider.val) + int(range_slider_2.val)])

        line4.set_ydata(cv_current[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line4.set_xdata(q_current[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line5.set_ydata(cv_prediction[int(range_slider.val) + int(range_slider_2.val)])
        line5.set_xdata(q_prediction[int(range_slider.val) + int(range_slider_2.val)])
        line6.set_ydata(cv_current[int(range_slider.val) + int(range_slider_2.val)])
        line6.set_xdata(q_current[int(range_slider.val) + int(range_slider_2.val)])
        fig.canvas.draw_idle()


    axs[0].set_ylim([-3, 3])
    axs[0].set_xlim([-3, 3])
    axs[1].set_ylim([-3, 3])
    axs[1].set_xlim([-3, 3])

    axs[0].set_xlabel('cv (pixel)')
    axs[0].set_ylabel('q (encoders)')
    axs[1].set_ylabel('cv (pixel)')
    axs[1].set_xlabel('q (encoders)')

    range_slider.on_changed(sliders_on_changed)
    range_slider_2.on_changed(sliders_on_changed)

    plt.show()



