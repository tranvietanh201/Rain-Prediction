import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# load data
data = 'data_cleaned.csv'
# import data
data = pd.read_csv(data)
# column list to choose from
column_list = ['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'WindGustDir',
               'WindGustSpeed', 'WindDir9am', 'WindDir3pm', 'WindSpeed9am',
               'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am',
               'Pressure3pm', 'Temp9am', 'Temp3pm', 'RainToday', 'RainTomorrow']

data1 = data.select_dtypes(include=['object'])
data1.drop(['Location'], axis=1, inplace=True)
data2 = data.select_dtypes(include=['float64'])

app = dash.Dash(__name__)

# ------------------------------------------------------------------------

app.layout = html.Div([

    html.Div([
        html.H1("1. Pie Chart"
                ),
        html.H2("Pie Chart of Rain in Australia Data", style={'textAlign': 'center'}
                ),
        dcc.Dropdown(
            id='my_dropdown',
            options=[{'label': s, 'value': s} for s in data1.columns],
            value='RainToday',
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
        dcc.Graph(id='my_graph', figure={}),
        html.H4(
            "The Pie Chart illustrates some features of the dataset such as Rain Possibility,"
            " or Wind Direction Distribution",
            style={'textAlign': 'center'}
        ),
        html.H4("Users can choose which features would be displayed by the dropdown box on the top left",
                style={'textAlign': 'center'}
                ),
        html.H4("Users can also download plot by clicking the camera icon on the top right",
                style={'textAlign': 'center'}
                ),
        dcc.ConfirmDialog(
            id='confirm_dialog',
            displayed=False,
            message='Please choose checklist variables!',
        ),
        html.H1("2. Scatter Matrix"
                ),
        html.H2("Scatter Matrix of Rain in Australia Data", style={'textAlign': 'center'}
                ),

        dcc.Checklist(
            id='my_checklist',
            options=[{'label': s, 'value': s} for s in data2.columns],
            value=['MinTemp', 'MaxTemp', 'Rainfall', 'WindGustSpeed'],
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="my_figure", figure={}),
    ]),
    html.H4(
        "The Scatter Matrix of dataset is displayed by the distribution of MinTemp and MaxTemp",
        style={'textAlign': 'center'}
    ),
    html.H4("Users can click the checkbox to decide which features would be shown",
            style={'textAlign': 'center'}
            ),
    html.H4("Some functions were also provided on the top right such as Zoom In, Box Select, or Auto Scale",
            style={'textAlign': 'center'}
            ),
    html.H4("Users can also move the mouse to any point of the graph to see hover detail",
            style={'textAlign': 'center'}
            ),
    html.H1("3. Multiple Line Chart"
            ),

    html.H2('Model Training Result Comparison', style={'textAlign': 'center'}),
    dcc.Graph(id='result',
              figure={
                  'data': [
                      {'x': ['Logistic Regression', 'Neural Network', 'Random Forest', 'Catboost', 'XGBoost'],
                       'y': [0.8406, 0.8524, 0.8514, 0.8493, 0.8554], 'type': 'line', 'name': 'Accuracy'},
                      {'x': ['Logistic Regression', 'Neural Network', 'Random Forest', 'Catboost', 'XGBoost'],
                       'y': [0.7016, 0.7296, 0.7180, 0.7310, 0.7446], 'type': 'line', 'name': 'ROC'},
                      {'x': ['Logistic Regression', 'Neural Network', 'Random Forest', 'Catboost', 'XGBoost'],
                       'y': [0.4629, 0.5147, 0.5000, 0.5110, 0.5356], 'type': 'line', 'name': "Cohen's Kappa"}
                  ],
                  'layout': {
                  }
              }),
    html.H4(
        "The Line Chart displayed the model training result of dataset like Accuracy, ROC, and Cohen's Kappa",
        style={'textAlign': 'center'}
    ),
    html.H4("Users can zoom in to see each line more clearly",
            style={'textAlign': 'center'}
            ),
    html.H4("Users can also move the mouse to any point of the graph to compare detail on hover",
            style={'textAlign': 'center'}
            ),
])


# ------------------------------------------------------------------------
@app.callback(
    Output('my_graph', 'figure'),

    Input('my_dropdown', 'value')
)
def update_graph(my_dropdown):
    dff = data1
    piechart = px.pie(
        dff,
        names=my_dropdown,
        hole=.3,
    )

    return piechart


@app.callback(
    Output('confirm_dialog', 'displayed'),
    Output('my_figure', 'figure'),

    Input('my_checklist', 'value'),
)
def update_graph(ckl_val):
    if len(ckl_val) > 0:
        fig = px.scatter_matrix(data2, dimensions=ckl_val, height=1300, color='MaxTemp',
                                hover_data={'MinTemp': True, 'MaxTemp': ':,'})
        fig.update_traces(diagonal_visible=False, showupperhalf=True, showlowerhalf=True)
        fig.update_layout(yaxis1={'title': {'font': {'size': 15}}}, yaxis2={'title': {'font': {'size': 15}}},
                          yaxis3={'title': {'font': {'size': 15}}}, yaxis4={'title': {'font': {'size': 15}}},
                          yaxis5={'title': {'font': {'size': 15}}}, yaxis6={'title': {'font': {'size': 15}}},
                          yaxis7={'title': {'font': {'size': 15}}}, yaxis8={'title': {'font': {'size': 15}}}
                          )
        fig.update_layout(xaxis1={'title': {'font': {'size': 15}}}, xaxis2={'title': {'font': {'size': 15}}},
                          xaxis3={'title': {'font': {'size': 15}}}, xaxis4={'title': {'font': {'size': 15}}},
                          xaxis5={'title': {'font': {'size': 15}}}, xaxis6={'title': {'font': {'size': 15}}},
                          xaxis7={'title': {'font': {'size': 15}}}, xaxis8={'title': {'font': {'size': 15}}}
                          )
        return False, fig

    if len(ckl_val) == 0:
        return True, dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True)
