import pandas as pd
import dash
from dash import dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import queue

created_files = queue.Queue()
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
                created_files.put(filepath)
                print(queue)

def get_last_file():
    if not created_files.empty():
        return created_files.get()
    else:
        return None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="FCM")

app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(dcc.Graph(id='main-plot'), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='ch1-plot'), width=6, lg=3),
            dbc.Col(dcc.Graph(id='ch2-plot'), width=6, lg=3),
            dbc.Col(dcc.Graph(id='ch3-plot'), width=6, lg=3),
            dbc.Col(dcc.Graph(id='ch4-plot'), width=6, lg=3),
        ]),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # 1 second
            n_intervals=0
        )
    ], fluid=True)


@app.callback(
    [Output('main-plot', 'figure'),
             Output('ch1-plot', 'figure'),
             Output('ch2-plot', 'figure'),
             Output('ch3-plot', 'figure'),
             Output('ch4-plot', 'figure')],
            [Input('interval-component', 'n_intervals')]
    )
def update_plots(n_intervals):
    filepath = get_last_file()
    if filepath:
        print(f"Plotting file: {filepath}")
        df = pd.read_csv(filepath)
        time = df.iloc[:, 0]
        ch_1 = df.iloc[:, 1]
        ch_2 = df.iloc[:, 2]
        ch_3 = df.iloc[:, 3]
        ch_4 = df.iloc[:, 4]

        main_plot = {
            'data': [
                go.Scatter(x=time, y=ch_1, mode='lines', name='CH 1', line=dict(color='red')),
                go.Scatter(x=time, y=ch_2, mode='lines', name='CH 2', line=dict(color='blue')),
                go.Scatter(x=time, y=ch_3, mode='lines', name='CH 3', line=dict(color='green')),
                go.Scatter(x=time, y=ch_4, mode='lines', name='CH 4', line=dict(color='magenta'))
            ],
            'layout': go.Layout(
                title='Field Cage Oscilloscope Monitoring',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }

        ch1_plot = {
            'data': [go.Scatter(x=time, y=ch_1, mode='lines', line=dict(color='red'))],
            'layout': go.Layout(
                title='Channel 1',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }

        ch2_plot = {
            'data': [go.Scatter(x=time, y=ch_2, mode='lines', line=dict(color='blue'))],
            'layout': go.Layout(
                title='Channel 2',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }

        ch3_plot = {
            'data': [go.Scatter(x=time, y=ch_3, mode='lines', line=dict(color='green'))],
            'layout': go.Layout(
                title='Channel 3',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }

        ch4_plot = {
            'data': [go.Scatter(x=time, y=ch_4, mode='lines', line=dict(color='magenta'))],
            'layout': go.Layout(
                title='Channel 4',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }

        return main_plot, ch1_plot, ch2_plot, ch3_plot, ch4_plot

# Run the app
if __name__ == '__main__':
    # Init the watching the given folder for new files.
    watch_path = "FC_mini_osc/monitoring_data/"
    event_handler = FileCreationHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=False)
    observer.start()

    try:
        app.run_server(debug=True)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        exit(0)
