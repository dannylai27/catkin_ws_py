import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
# from read_bag import load_all_experiments
from bagpy import bagreader
import pandas as pd
from matplotlib.widgets import Slider
import numpy as np

if __name__ == "__main__":

    fig, axs = plt.subplots(1, 2)

    file_folder = '/home/cflai/catkin_ws_py/bag_file/norm_val/multi_future_prediction/'
    trial_files = [f for f in listdir(file_folder) if isfile(join(file_folder, f))]
    # trial_results = load_all_experiments(file_folder, file_folder + 'validation/')

    for name in trial_files:
        bag_list = []
        b = bagreader(file_folder + name)
        bag_list.append(b)
        print(name)

    norm_val = bag_list[0].message_by_topic('/norm_val')
    df = pd.read_csv(norm_val)
    time = df['Time'].tolist()
    cv_new_1 = df['data_0'].tolist()
    cv_new_2 = df['data_1'].tolist()
    cv_new_3 = df['data_2'].tolist()
    cv_old = df['data_3'].tolist()
    q_new_1 = df['data_4'].tolist()
    q_new_2 = df['data_5'].tolist()
    q_new_3 = df['data_6'].tolist()
    q_old = df['data_7'].tolist()

    df['cv_new'] = df[['data_0', 'data_1', 'data_2']].values.tolist()
    df['q_new'] = df[['data_4', 'data_5', 'data_6']].values.tolist()

    cv_new = df['cv_new'].tolist()
    q_new = df['q_new'].tolist()

    starting_point = 200
    time_width = 10

    [line] = axs[0].plot(cv_old[starting_point:starting_point + time_width],
                         q_old[starting_point:starting_point + time_width],
                         marker='o', label='historical features')
    [line2] = axs[0].plot(cv_new[starting_point + time_width],
                          q_new[starting_point + time_width],
                          marker='x', label='future prediction')
    [line3] = axs[0].plot(cv_old[starting_point + time_width],
                          q_old[starting_point + time_width],
                          marker='+', label='true future label')
    [line4] = axs[1].plot(q_old[starting_point:starting_point + time_width],
                          cv_old[starting_point:starting_point + time_width],
                          marker='o', label='ground truth')
    [line5] = axs[1].plot(q_new[starting_point + time_width],
                          cv_new[starting_point + time_width],
                          marker='x', label='prediction')
    [line6] = axs[1].plot(q_old[starting_point + time_width],
                          cv_old[starting_point + time_width],
                          marker='+', label='prediction')

    range_slider_ax = fig.add_axes([0.25, 0.03, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    range_slider = Slider(range_slider_ax, 'range', 0, 500, valinit=starting_point)
    range_slider_ax_2 = fig.add_axes([0.25, 0.005, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    range_slider_2 = Slider(range_slider_ax_2, 'range', 0, 500, valinit=time_width)


    def sliders_on_changed(val):
        line.set_xdata(cv_old[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line.set_ydata(q_old[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line2.set_xdata(cv_new[int(range_slider.val) + int(range_slider_2.val)])
        line2.set_ydata(q_new[int(range_slider.val) + int(range_slider_2.val)])
        line3.set_xdata(cv_old[int(range_slider.val) + int(range_slider_2.val)])
        line3.set_ydata(q_old[int(range_slider.val) + int(range_slider_2.val)])

        line4.set_ydata(cv_old[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line4.set_xdata(q_old[int(range_slider.val): int(range_slider.val) + int(range_slider_2.val)])
        line5.set_ydata(cv_new[int(range_slider.val) + int(range_slider_2.val)])
        line5.set_xdata(q_new[int(range_slider.val) + int(range_slider_2.val)])
        line6.set_ydata(cv_old[int(range_slider.val) + int(range_slider_2.val)])
        line6.set_xdata(q_old[int(range_slider.val) + int(range_slider_2.val)])

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
