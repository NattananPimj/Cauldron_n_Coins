
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# TODO: process data here
class DataApp(ttk.Frame):
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

    def create_widgets(self):
        # creating a row with combobox widgets for filters
        self.frame_dist = ttk.LabelFrame(self, text="Select Distribution")
        self.frame_dist.grid(row=1, column=0, sticky="NEWS")

        self.cb_dist = ttk.Combobox(self.frame_dist, state="readonly")
        self.cb_dist['values'] = (
            'Normal',
            'Exponential',
            'Uniform',
        )
        self.cb_dist.bind('<<ComboboxSelected>>', self.update_dist)
        self.cb_dist.grid(row=0, column=0, padx=10, pady=10)

        self.btn_quit = ttk.Button(self, text="Quit", command=root.destroy)
        self.btn_quit.grid(row=2, column=0, pady=10)
        self.btn_quit = ttk.Button(self, text="Quit", command=root.destroy)

        ## create Matplotlib figure and plotting axes
        self.fig_hist = Figure()
        self.ax_hist = self.fig_hist.add_subplot()

        # create a canvas to host the figure and place it into the main window
        self.fig_canvas = FigureCanvasTkAgg(self.fig_hist, master=self)
        self.fig_canvas.get_tk_widget().grid(row=0, column=0,
                                             sticky="news", padx=10, pady=10)

    def update_dist(self, ev):
        dist = self.cb_dist.get()
        if dist == 'Normal':
            self.data = np.random.normal(size=10000)
        elif dist == 'Exponential':
            self.data = np.random.exponential(size=10000)
        elif dist == 'Uniform':
            self.data = np.random.uniform(size=10000)
        self.update_plot()

    def use_of_herb(self):
        pass

    def update_plot(self):
        self.ax_hist.clear()
        self.ax_hist.hist(self.data, bins=20)
        self.ax_hist.set_xlabel("x")
        self.ax_hist.set_ylabel("frequency")
        self.fig_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Matplotlib Integration")
    root.geometry("600x600")
    app = DataApp(root)
    root.mainloop()
