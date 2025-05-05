import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
import matplotlib.pyplot as plt
import csv
import pandas as pd
from cnc_config import Config

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# TODO: process data here
class DataApp(ttk.Frame):
    __herb_id = ['01', '02', '03', '04', '05', '06', '07', '08',
                 '09', '10', '11', '12', '13', '14', '15', '16']

    __filename = {
        'herb_use': 'herb_use.csv',
        'herb_potion': 'herb_each_potion.csv',
        'distance': 'potion_distance.csv',
        'haggle_information': 'haggle_fail.csv',
        'sell_success': 'sell_success.csv',
    }
    # TODO: add sell info

    def __init__(self, parent):
        super().__init__(parent)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()
        self.data = None

        self.__data_base = {}
        self.load_data_base()

    def create_widgets(self):
        # creating a row with combobox widgets for filters
        self.frame_dist = ttk.LabelFrame(self, text="Select Distribution")
        self.frame_dist.grid(row=1, column=0, sticky="NEWS")

        self.cb_dist = ttk.Combobox(self.frame_dist, state="readonly")
        self.cb_dist['values'] = (
            'herb use',
            'herb potion',
            'distance',
            'sell success',
            'haggle information'
        )
        self.cb_dist.bind('<<ComboboxSelected>>', self.update_dist)
        self.cb_dist.grid(row=0, column=0, padx=10, pady=10)

        self.btn_quit = ttk.Button(self, text="Quit", command=root.destroy)
        self.btn_quit.grid(row=2, column=0, pady=10)
        self.btn_quit = ttk.Button(self, text="Quit", command=root.destroy)

        # create Matplotlib figure and plotting axes
        self.fig_graph = Figure()
        self.fig_graph.set_size_inches(10, 6)
        self.ax_graph = self.fig_graph.add_subplot()

        # create a canvas to host the figure and place it into the main window
        self.fig_canvas = FigureCanvasTkAgg(self.fig_graph, master=self)
        self.fig_canvas.get_tk_widget().grid(row=0, column=0,
                                             sticky="news", padx=10, pady=10)

    def update_dist(self, ev):
        dist = self.cb_dist.get()
        if dist == 'herb use':
            self.process_herb_use()
        elif dist == 'herb potion':
            self.data = np.random.exponential(size=10000)
        elif dist == 'distance':
            self.process_potion_distance()
        elif dist == 'sell success':
            self.process_sell_success()
        elif dist == 'haggle information':
            self.process_haggle_information()
        # self.update_plot()

    def load_data_base(self):
        for key, value in self.__filename.items():
            self.__data_base[key] = pd.read_csv('database/' + value)

    def process_herb_use(self):
        self.ax_graph.clear()
        data = self.__data_base['herb_use']
        tmpx = []
        tmpy = []
        # print(data)
        for i in range(1, 17):
            tmpx.append(f"{Config.HERB_INFO[self.__herb_id[i - 1]]['name']}")
            tmpy.append(len(data[data['ID'] == i]))
        # print(tmpx, tmpy)
        color = ['red', 'blue', 'green', 'yellow', 'cyan']
        self.ax_graph.bar(tmpx, tmpy, color=color, width=0.6)
        self.ax_graph.set_xticklabels(tmpx, rotation=75, ha='right')
        # TODO: change axis label+ add y ticks + add color and legend
        self.ax_graph.set_xlabel("x")
        self.ax_graph.set_ylabel("frequency")
        self.ax_graph.set_title("Herb use")
        self.fig_graph.subplots_adjust(top=0.9, bottom=0.25)

        self.fig_canvas.draw()

    def process_potion_distance(self):
        # TODO: add axis label and ticks
        self.ax_graph.clear()
        dfline = pd.DataFrame.from_dict(Config.POTION_DISPLACEMENT, orient="index")
        self.ax_graph.plot(dfline.index, dfline[0], color='m')

        df = self.__data_base['distance']
        for tier in df['Tier'].unique():
            subset = df[df['Tier'] == tier]
            self.ax_graph.scatter(subset['Potion'], subset['Distance'],
                                  label=tier)
        self.ax_graph.set_xticklabels(dfline.index, rotation=45, ha='right')
        self.ax_graph.legend()
        self.ax_graph.set_title("Distance in each potion")
        self.fig_graph.subplots_adjust(top=0.9, bottom=0.25)

        self.fig_canvas.draw()

    def process_haggle_information(self):
        # TODO: set axis and label
        self.ax_graph.clear()
        data = self.__data_base['haggle_information'].groupby('Speed')['Success'].mean()
        speed = [1, 2, 3]
        percent = [data[i] for i in speed]
        self.ax_graph.bar(speed, percent, color='m')

        self.fig_canvas.draw()

    def process_sell_success(self):
        self.ax_graph.clear()
        df = pd.DataFrame(self.__data_base['sell_success'])
        bins = np.arange(1, 12, 1)
        width = 0.4

        success_trials = df[df["Success"] == 1]["Trial"].values
        fail_trials = df[df["Success"] == 0]["Trial"].values
        hist_success, _ = np.histogram(success_trials, bins=bins)
        print(success_trials)
        print(hist_success)
        hist_fail, _ = np.histogram(fail_trials, bins=bins)

        self.ax_graph.bar(bins[:-1] - width / 2, hist_success, width=width, label="Success", color="blue", edgecolor="black")
        self.ax_graph.bar(bins[:-1] + width / 2, hist_fail, width=width, label="Fail", color="red", edgecolor="black")

        self.ax_graph.set_xlabel("Trials until Success/Fail")
        self.ax_graph.set_ylabel("Frequency")
        self.ax_graph.set_title("Histogram of Trials until Success or Failure")
        self.ax_graph.set_xticks(range(1, 11))  # Ensures clear labeling of bins 1-10
        self.ax_graph.legend()

        self.fig_canvas.draw()





    def update_plot(self):
        self.ax_graph.clear()
        self.ax_graph.hist(self.data, bins=20)
        self.ax_graph.set_xlabel("x")
        self.ax_graph.set_ylabel("frequency")
        self.fig_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matplotlib Integration")
    root.geometry("1000x720")
    app = DataApp(root)
    root.mainloop()
    app.process_herb_use()
