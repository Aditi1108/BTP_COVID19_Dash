import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import datetime

# Load data
Pos_df = pd.read_excel('data/Data.xlsx')

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

#  plot_bgcolor='rgb(10,10,10)'                


app.layout = html.Div(
    children = [
    html.Div(
        children = [
        html.Div(
            className = 'row1',
            children=[
                html.Div(
                    className='four columns div-user-controls',
                    children=[
                        html.H2('Positive OR Negative Tweets per Country per Day'),
                        html.P('Pick one sentiment from the dropdown below.'),
                        dcc.Dropdown(
                        id='Emotion',
                        options=[
                            {'label': 'Positive', 'value': 'Positive'},
                            {'label': 'Negative', 'value': 'Negative'}
                        ],
                        value='Positive',
                        clearable=False
                        ),
                        html.P('Pick one month from the dropdown below.'),
                        dcc.Dropdown(
                        id='Month',
                        options=[
                            {'label': 'March', 'value': 'March'},
                            {'label': 'April', 'value': 'April'},
                            {'label': 'May', 'value': 'May'}
                        ],
                        value='March',
                        clearable=False
                        )
                    ]
                ),
                html.Div(
                    className='eight columns div-for-charts bg-grey',
                    children=[
                        dcc.Graph(id='BarPlot', animate=True)
                ])
            ]),
        html.Div(
            className = 'row2',
            children = [
                html.Div(
                className='four columns div-user-controls',
                children=[
                    html.H2('Total positive and negative tweets per day'),
                    html.P('Pick one month from the dropdown below.'),
                    dcc.Dropdown(
                    id='MonthSel',
                    options=[
                        {'label': 'March', 'value': 'March'},
                        {'label': 'April', 'value': 'April'},
                        {'label': 'May', 'value': 'May'}
                    ],
                    value='March',
                    clearable=False
                    )
                ]
            ),
            html.Div(
                className = 'eight columns div-for-charts',
                children=[
                    dcc.Graph(id='LinePlot', animate=True)
            ])
        ])
    ])
])

mapVal = {'March' : 3, 'April' : 4, 'May' : 5}


@app.callback(Output('LinePlot', 'figure'),
              [Input('MonthSel', 'value')])
def update_lineplot(value):
    df = Pos_df[pd.to_datetime(Pos_df['Date']).dt.month == mapVal[value]]
    df = df.groupby(['Date', 'Sentiment'], as_index = False, sort = True).aggregate({'Frequency': 'sum'})
    linefig = px.line(df, x="Date", y="Frequency", color='Sentiment', color_discrete_map={
        "Negative": "red", "Positive": "green"})
    linefig.update_xaxes(showgrid=False, zeroline=False)
    linefig.update_yaxes(showgrid=False, zeroline=False)
    date = datetime.datetime(2020, mapVal[value], 1)
    previous_Date = date - datetime.timedelta(days=1)
    linefig.update_layout(xaxis_range=[previous_Date,
                               datetime.datetime(2020, mapVal[value] + 1, 1)])
    return linefig

@app.callback(Output('BarPlot', 'figure'),
              [Input('Month', 'value'),Input('Emotion', 'value')])
def update_graph(value,emo):

    df = Pos_df[Pos_df['Sentiment'] == emo]
    df = df[pd.to_datetime(df['Date']).dt.month == mapVal[value ]]
    df = df.groupby(['Date','Country'], as_index = False, sort = True).aggregate({'Frequency': 'sum'})
    
    fig = px.bar(df, x="Date", y="Frequency", color="Country")
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    date = datetime.datetime(2020, mapVal[value], 1)
    previous_Date = date - datetime.timedelta(days=1)
    fig.update_layout(xaxis_range=[previous_Date,
                               datetime.datetime(2020, mapVal[value] + 1, 1)])
   
    colors = {
        'background': '#31302F',
        'text': '#FFFFFF'
    }

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        bargap=0.22
        )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
