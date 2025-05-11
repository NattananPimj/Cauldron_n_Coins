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


class DataApp(ttk.Frame):
    __herb_id = ['01', '02', '03', '04', '05', '06', '07', '08',
                 '09', '10', '11', '12', '13', '14', '15', '16']

    __filename = {
        'herb_use': 'herb_use.csv',
        'potion_profit': 'potion_profit.csv',
        'distance': 'potion_distance.csv',
        'haggle_information': 'haggle_fail.csv',
        'sell_success': 'sell_success.csv',
    }

    def __init__(self, parent):
        super().__init__(parent)
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.__parent = parent
        self.__parent.title("Game Statistics")
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()

        self.__data_base = {}
        self.load_data_base()

    def create_widgets(self):
        self.frame_graph = ttk.LabelFrame(self, text="Select Statistic")
        self.frame_graph.grid(row=1, column=0, sticky="NEWS")

        self.choice = ttk.Combobox(self.frame_graph, state="readonly")
        self.choice['values'] = (
            'herb use',
            'potion profit',
            'distance',
            'sell success',
            'haggle information'
        )
        self.choice.bind('<<ComboboxSelected>>', self.update_dist)
        self.choice.grid(row=0, column=0, padx=10, pady=10)

        self.btn_quit = ttk.Button(self, text="Quit", command=self.__parent.destroy)
        self.btn_quit.grid(row=2, column=0, pady=10)
        self.btn_quit = ttk.Button(self, text="Quit", command=self.__parent.destroy)

        # create Matplotlib figure and plotting axes
        self.fig_graph = Figure()
        self.fig_graph.set_size_inches(10, 6)
        self.ax_graph = self.fig_graph.add_subplot()

        # create a canvas
        self.fig_canvas = FigureCanvasTkAgg(self.fig_graph, master=self)
        self.fig_canvas.get_tk_widget().grid(row=0, column=0,
                                             sticky="news", padx=10, pady=10)

    def update_dist(self, ev):
        dist = self.choice.get()
        if dist == 'herb use':
            self.process_herb_use()
        elif dist == 'potion profit':
            self.process_potion_profit()
        elif dist == 'distance':
            self.process_potion_distance()
        elif dist == 'sell success':
            self.process_sell_success()
        elif dist == 'haggle information':
            self.process_haggle_information()
        # self.update_plot()

    def load_data_base(self):
        for key, value in self.__filename.items():
            self.__data_base[key] = pd.DataFrame(pd.read_csv('database/' + value))

    def process_herb_use(self):
        self.ax_graph.clear()
        data = self.__data_base['herb_use']
        tmpx = []
        tmpy = []
        lb = []
        # print(data)
        for i in range(1, 17):
            tmpx.append(f"{Config.HERB_INFO[self.__herb_id[i - 1]]['name']}")
            tmpy.append(len(data[data['ID'] == i]))
            lb.append(Config.HERB_INFO[self.__herb_id[i - 1]]['direction'])
        # print(tmpx, tmpy)
        color = ['red', 'red', 'blue', 'blue', 'green', 'green', 'yellow', 'yellow',
                 'cyan', 'cyan', 'm', 'm', 'gray', 'gray', 'chocolate', 'chocolate']
        # self.ax_graph.bar(tmpx, tmpy, color=color, width=0.6, label=lb)

        for i in range(0, 16, 2):
            self.ax_graph.bar(tmpx[i], tmpy[i], color=color[i], width=0.6, label=lb[i])
            self.ax_graph.bar(tmpx[i+1], tmpy[i+1], color=color[i+1], width=0.6)

        self.ax_graph.set_xticks(tmpx)
        self.ax_graph.set_xticklabels(tmpx, rotation=75, ha='right')
        self.ax_graph.set_xlabel("Herbs")
        self.ax_graph.set_ylabel("frequency")
        self.ax_graph.set_title("Overall herb use")
        self.ax_graph.legend(title='Direction')
        self.fig_graph.subplots_adjust(top=0.9, bottom=0.25)

        self.fig_canvas.draw()

    def process_potion_profit(self):
        self.ax_graph.clear()

        df = self.__data_base['potion_profit']
        self.ax_graph.set_title("Potion Profit")
        gb = df.groupby('Potion')
        # print(df['Potion'].unique())

        columns = ['Potion', 'Average Price($)', 'Average Cost($)', 'Average Profit($)']
        data = [[p, f"{gb['Sellprice'].mean()[p]:.2f}", f"{gb['Cost'].mean()[p]:.2f}", f"{gb['Profit'].mean()[p]:.2f}"]
                for p in df.Potion.unique()]

        # Hide the axes
        self.ax_graph.set_axis_off()

        # Create the table
        table = self.ax_graph.table(cellText=data, colLabels=columns, loc='center', cellLoc='right')

        # Adjust the table's layout
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        self.fig_canvas.draw()

    def process_potion_distance(self):
        self.ax_graph.clear()
        dfline = pd.DataFrame.from_dict(Config.POTION_DISPLACEMENT, orient="index")
        self.ax_graph.plot(dfline.index, dfline[0], color='m', label='Displacement from start')

        df = self.__data_base['distance']
        for tier in [1, 2, 3]:
            subset = df[df['Tier'] == tier]
            self.ax_graph.scatter(subset['Potion'], subset['Distance'],
                                  label=tier)
        self.ax_graph.set_xticks(dfline.index)
        self.ax_graph.set_xticklabels(dfline.index, rotation=45, ha='right')
        self.ax_graph.legend(title='Tier of potion')
        self.ax_graph.set_title("Distance in each potion")

        self.ax_graph.set_xlabel("Potion")
        self.ax_graph.set_ylabel("Distance")
        self.ax_graph.set_title("Distance take to create a potion")

        self.fig_graph.subplots_adjust(top=0.9, bottom=0.25)

        self.fig_canvas.draw()

    def process_haggle_information(self):
        self.ax_graph.clear()
        data = self.__data_base['haggle_information'].groupby('Speed')['Success'].mean()
        speed = ['1', '2', '3']
        percent = [data[int(i)] for i in speed]
        bar = self.ax_graph.bar(speed, percent, color='m')

        self.ax_graph.set_title("Haggle Success Rate in each speed")
        self.ax_graph.set_xlabel("speed")
        self.ax_graph.set_ylabel("Success percent")
        self.ax_graph.bar_label(bar, fmt='%.2f')

        self.fig_canvas.draw()

    def process_sell_success(self):
        self.ax_graph.clear()
        df = self.__data_base['sell_success']
        bins = np.arange(1, 12, 1)
        width = 0.4

        success_trials = df[df["Success"] == 1]["Trial"].values
        fail_trials = df[df["Success"] == 0]["Trial"].values
        hist_success, _ = np.histogram(success_trials, bins=bins)
        # print(success_trials)
        # print(hist_success)
        hist_fail, _ = np.histogram(fail_trials, bins=bins)

        self.ax_graph.bar(bins[:-1] - width / 2, hist_success, width=width, label="Success", color="blue",
                          edgecolor="black")
        self.ax_graph.bar(bins[:-1] + width / 2, hist_fail, width=width, label="Fail", color="red", edgecolor="black")

        self.ax_graph.set_xlabel("Trials until Success/Fail")
        self.ax_graph.set_ylabel("Frequency")
        self.ax_graph.set_title("Histogram of Trials until Success or Failure")
        self.ax_graph.set_xticks(range(1, 11))  # Ensures clear labeling of bins 1-10
        self.ax_graph.legend()

        self.fig_canvas.draw()


if __name__ == "__main__":
    a = tk.Tk()
    a.title("Matplotlib Integration")
    a.geometry("1000x720")
    app = DataApp(a)
    a.mainloop()
    # app.process_herb_use()
