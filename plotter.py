"""
Created on 2024/06/18
Author: Alicia Vázquez-Ramos
E-mail: aliciavr@ugr.es
Description: Plot the four channels of the oscilloscope monitoring the Field Cage.
The plot is updated when a new file is created.
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import queue

class FileCreationHandler(FileSystemEventHandler):
    def __init__(self):
        self.created_files = queue.Queue()

    def on_created(self, event):
        if not event.is_directory:
            #psplit = event.src_path.split(".")
            #filepath = psplit[0] + psplit[1] + "." + psplit[2]
            filepath = event.src_path
            if filepath.endswith(".csv"):
                print(f"New file detected: {filepath}")
                self.created_files.put(filepath)

    def get_last_file(self):
        if not self.created_files.empty():
            return self.created_files.get()
        else:
            return None

def update_plot(frame, event_handler, fig, gs):
    filepath = event_handler.get_last_file()
    if filepath:
        fig.clear()
        plot(filepath, fig, gs)


def plot(filepath, fig, gs):

    df = pd.read_csv(filepath)

    time = df.iloc[:, 0]
    ch_1 = df.iloc[:, 1]
    ch_2 = df.iloc[:, 2]
    ch_3 = df.iloc[:, 3]
    ch_4 = df.iloc[:, 4]

    # Main plot
    ax1 = fig.add_subplot(gs[:, :2])
    ax1.plot(time, ch_1, label="CH 1", color="r")
    ax1.plot(time, ch_2, label="CH 2", color="b")
    ax1.plot(time, ch_3, label="CH 3", color="g")
    ax1.plot(time, ch_4, label="CH 4", color="m")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Voltage [V]")
    ax1.set_title("Field Cage Oscilloscope Monitoring")

    # Plot CH 1
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.plot(time, ch_1, color="r")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Voltage [V]")
    ax2.set_title("Channel 1")

    # Plot CH 2
    ax3 = fig.add_subplot(gs[0, 3])
    ax3.plot(time, ch_2, color="b")
    ax3.set_xlabel("Time [s]")
    ax3.set_ylabel("Voltage [V]")
    ax3.set_title("Channel 2")

    # Plot CH 3
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.plot(time, ch_3, color="g")
    ax4.set_xlabel("Time [s]")
    ax4.set_ylabel("Voltage [V]")
    ax4.set_title("Channel 3")

    # Plot CH 4
    ax5 = fig.add_subplot(gs[1, 3])
    ax5.plot(time, ch_4, color="m")
    ax5.set_xlabel("Time [s]")
    ax5.set_ylabel("Voltage [V]")
    ax5.set_title("Channel 4")

    plt.tight_layout(pad=2.5)

    plt.draw()

if __name__ == "__main__":

    fig = plt.figure(figsize=(16, 8))
    gs = GridSpec(2, 4, figure=fig, width_ratios=[3, 1, 1, 1])

    watch_path = "FC_mini_osc/monitoring_data/"
    #watch_path = "FC_mini_osc/triggered_data/"
    event_handler = FileCreationHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=False)
    observer.start()

    ani = FuncAnimation(fig, update_plot, fargs=(event_handler, fig, gs), interval=50)

    try:
        plt.show()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        plt.close()
        exit(0)
