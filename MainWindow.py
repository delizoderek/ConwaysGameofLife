import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.colors as colors
import matplotlib.animation as animation


class MainWindow:
    def __init__(self):
        self.n = 10
        self.ON = 255
        self.OFF = 0
        self.vals = [self.ON, self.OFF]
        self.pause = True
        self.root = tk.Tk()
        self.create_frames()
        self.create_graph()
        self.buttons()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=1)
        self.root.minsize(500, 300)
        self.root.geometry("800x600")
        self.root.state("zoomed")
        self.root.mainloop()

    def create_frames(self):
        self.left_frame = tk.Frame(
            self.root,
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self.root, bg="green")
        self.right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.plot_frame = tk.Frame(self.left_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def create_graph(self):
        self.grid = self.randomGrid()
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.im = self.ax.imshow(self.grid, interpolation='nearest')
        self.fig_canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ax.set_xticks(np.arange(self.n))
        self.ax.set_yticks(np.arange(self.n))
        self.ax.set_xticklabels(np.arange(1, self.n + 1))
        self.ax.set_yticklabels(np.arange(1, self.n + 1))
        self.ax.set_aspect("equal")

        self.cid = self.fig_canvas.mpl_connect("button_press_event", self.invert_square)

        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.plot_frame)
        self.toolbar.update()
        self.fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ani = animation.FuncAnimation(
            self.fig, self.update, np.arange(1, 200), interval=25, blit=False
        )

    def buttons(self):
        self.button_frame = tk.Frame(self.right_frame)
        self.button_frame.grid(row=0, column=0)

        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        self.label = tk.Label(self.button_frame, text="Grid Size:")
        self.entry = tk.Entry(self.button_frame, font=12)
        self.setGridSize = tk.Button(
            self.button_frame,
            text="Set Grid Size",
            width=20,
            command=self.set_grid_size,
        )
        self.startBtn = tk.Button(
            self.button_frame, text="Start", width=20, command=self.start_animation
        )
        self.randomize = tk.Button(
            self.button_frame, text="Randomize", width=20, command=self.randomize_grid
        )
        self.reset = tk.Button(
            self.button_frame, text="Reset", width=20, command=self.reset_grid
        )

        self.label.grid(row=0, column=0)
        self.entry.grid(row=1, column=0)
        self.setGridSize.grid(row=2, column=0)
        self.startBtn.grid(row=3, column=0)
        self.randomize.grid(row=4, column=0)
        self.reset.grid(row=5, column=0)

    def randomGrid(self):
        """returns a grid of NxN random values"""
        return np.random.choice(self.vals, self.n * self.n, p=[0.2, 0.8]).reshape(
            self.n, self.n
        )

    def invert_square(self, event):
        if event.inaxes == self.ax:
            x, y = int(round(event.xdata)), int(round(event.ydata))
            self.grid[y, x] = 255 - self.grid[y, x]
            self.ax.imshow(self.grid, interpolation='nearest')
            self.fig_canvas.draw()

    def set_grid_size(self):
        self.n = int(self.entry.get())
        self.grid = np.random.randint(0, 2, (self.n, self.n))
        self.im = self.ax.imshow(self.grid, interpolation='nearest')
        self.fig_canvas.draw()

        self.ax.set_xticks(np.arange(self.n))
        self.ax.set_yticks(np.arange(self.n))
        self.ax.set_xticklabels(np.arange(1, self.n + 1))
        self.ax.set_yticklabels(np.arange(1, self.n + 1))

        self.cid = self.fig_canvas.mpl_connect("button_press_event", self.invert_square)

    def update(self, frameNum):
        if self.pause:
            return

        N = self.n
        newGrid = self.grid.copy()
        for i in range(N):
            for j in range(N):
                # compute 8-neghbor sum
                total = int(
                    (
                        self.grid[i, (j - 1) % N]
                        + self.grid[i, (j + 1) % N]
                        + self.grid[(i - 1) % N, j]
                        + self.grid[(i + 1) % N, j]
                        + self.grid[(i - 1) % N, (j - 1) % N]
                        + self.grid[(i - 1) % N, (j + 1) % N]
                        + self.grid[(i + 1) % N, (j - 1) % N]
                        + self.grid[(i + 1) % N, (j + 1) % N]
                    )
                    / 255
                )

                # apply Conway's rules
                if self.grid[i, j] == self.ON:
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = self.OFF
                else:
                    if total == 3:
                        newGrid[i, j] = self.ON

        self.ax.clear()  # Clear the previous frame
        self.grid[:] = newGrid[:]
        self.im = self.ax.imshow(self.grid, interpolation='nearest')
        self.fig_canvas.draw()

        return self.im

    def start_animation(self):
        if self.pause:
            self.startBtn.config(text="Stop")
            self.pause = False
        else:
            self.startBtn.config(text="Start")
            self.pause = True

    def randomize_grid(self):
        self.grid = np.random.randint(0, 2, (self.n, self.n))
        self.ax.imshow(self.grid, interpolation='nearest')
        self.fig_canvas.draw()

    def reset_grid(self):
        self.grid = np.full((self.n, self.n), self.OFF)
        self.ax.imshow(self.grid, interpolation='nearest')
        self.fig_canvas.draw()


if __name__ == "__main__":
    MainWindow()
