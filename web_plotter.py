import dash
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd

# Create plots
def create_plots(filepath):
    # Read data
    df = pd.read_csv(filepath)

    # Get data
    time = df.iloc[:, 0]
    ch_1 = df.iloc[:, 1]
    ch_2 = df.iloc[:, 2]
    ch_3 = df.iloc[:, 3]
    ch_4 = df.iloc[:, 4]
    main_plot = dcc.Graph(
        id='main-plot',
        figure={
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
    )

    ch1_plot = dcc.Graph(
        id='ch1-plot',
        figure={
            'data': [go.Scatter(x=time, y=ch_1, mode='lines', line=dict(color='red'))],
            'layout': go.Layout(
                title='Channel 1',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }
    )

    ch2_plot = dcc.Graph(
        id='ch2-plot',
        figure={
            'data': [go.Scatter(x=time, y=ch_2, mode='lines', line=dict(color='blue'))],
            'layout': go.Layout(
                title='Channel 2',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }
    )

    ch3_plot = dcc.Graph(
        id='ch3-plot',
        figure={
            'data': [go.Scatter(x=time, y=ch_3, mode='lines', line=dict(color='green'))],
            'layout': go.Layout(
                title='Channel 3',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }
    )

    ch4_plot = dcc.Graph(
        id='ch4-plot',
        figure={
            'data': [go.Scatter(x=time, y=ch_4, mode='lines', line=dict(color='magenta'))],
            'layout': go.Layout(
                title='Channel 4',
                xaxis={'title': 'Time [s]'},
                yaxis={'title': 'Voltage [V]'}
            )
        }
    )

    return main_plot, ch1_plot, ch2_plot, ch3_plot, ch4_plot

# Define app layout
def create_layout(app, main_plot: object, ch1_plot: object, ch2_plot: object, ch3_plot: object, ch4_plot: object) -> object:
    app.layout = dbc.Container([

        dbc.Row([
            dbc.Col(main_plot, width=12),
        ]),

        dbc.Row([
            dbc.Col(ch1_plot, width=6, lg=3),
            dbc.Col(ch2_plot, width=6, lg=3),
            dbc.Col(ch3_plot, width=6, lg=3),
            dbc.Col(ch4_plot, width=6, lg=3),
        ])
    ], fluid=True)


# Run the app
if __name__ == '__main__':
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="FCM")

    filepath = "FC_mini_osc/triggered_data/oscilloscope_data_1718742368-7585113_ALL.csv"
    main_plot, ch1_plot, ch2_plot, ch3_plot, ch4_plot = create_plots(filepath)

    create_layout(app, main_plot, ch1_plot, ch2_plot, ch3_plot, ch4_plot)

    app.run_server(debug=True)
