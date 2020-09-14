import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go

import plotly.express as px

import pandas as pd
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])
senti_df = pd.read_csv('data/Number_emotion.csv')
pos_df = pd.read_csv('data/pos_neg.csv')

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

##Table for bar chart for total sentimnet 
x_bar = ['Anger', 'Fear','Analytical','Joy','Sadness']
y_bar = [senti_df['anger_output'].sum(), senti_df['fear_output'].sum(), senti_df['analytical_output'].sum(), senti_df['joy_output'].sum(), senti_df['sadness_output'].sum()]
fig_bar = go.Figure(data=[go.Bar(
            x=x_bar, y=y_bar,
            #colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
            text=y_bar,
            textposition='auto',
            marker =  {'color': ['#b50000','#037357', '#375CB1','#d4bc81','#a267cf', '#FF4F00','#FF0056','#5E0DAC',  ]}
        )])
fig_bar.update_layout(
                #colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin={'b': 15},
                hovermode='x',
                autosize=True,
                title={'text': 'Overall Recorded Sentiments', 'font': {'color': 'white'}, 'x': 0.5},
                #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
                xaxis_title="Emotions",
                yaxis_title="Count",
)
##Table for pie chart of pos neg neutral
labels_pie = ['Positive','Neutral','Negative']
values_pie = [pos_df['Positive'].sum(),pos_df['Neutral'].sum(),pos_df['Negative'].sum()]
fig_pie = go.Figure(data=[go.Pie(labels=labels_pie, values=values_pie)])
fig_pie.update_layout(
                colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin={'t': 50},
                hovermode='x',
                height = 300,
                #autosize=True,
                title={'text': 'Polarity of recorded Tweets', 'font': {'color': 'white'}, 'x': 0.5},
                #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
)

app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('DASH - STOCK PRICES'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
                                                      multi=True, value=[df['stock'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                             html.Div(className = 'row',
                                children = [
                                 html.Div(className = 'four columns',
                                    children = [
                                    html.Div(className = 'div-user-controls-small ',
                                        children=[
                                            html.H2('POSITIVE, NEGATIVE AND NEUTRAL SENTIMENTS'),
                                            html.P('Pick one or more sentiment from the dropdown below.'),
                                            html.Div(
                                                className='div-for-dropdown',
                                                    children=[
                                                                dcc.Dropdown(id='Sentimentselector',
                                                                        options=[{'label' : 'Positive', 'value': 'Positive'},
                                                                                            {'label':'Neutral','value':'Neutral'},
                                                                                            {'label':'Negative','value':'Negative'} 
                                                                                ],
                                                                        multi=True, value=['Positive','Negative'],
                                                                        style={'backgroundColor': '#1E1E1E'}, #colour '#1E1E1E'
                                                                        className='Sentimentselector'
                                                                    ),
                                                            ],
                                                    style={'color': '#1E1E1E'})
                                                ]
                                            ),             
                                    html.Div(className = 'div-for-charts_small bg-grey',
                                        children = [
                                            dcc.Graph(id = 'pie_graph',
                                            config={'displayModeBar': False},
                                            animate =True,
                                            figure = fig_pie
                                            )],
                    
                                        ),
                                    ]),

                            html.Div(className = 'eight_half columns div-for-charts bg-grey',
                                children = [
                                    dcc.Graph(id = 'pos_neg_graph',
                                    config={'displayModeBar': False},
                                    animate =True,
                                    #figure = fig_posneg 
                                    )
                                ]),
                            ]
                        ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True)
                             ]),
                    html.Div(className = 'four columns div-for-charts bg-grey',
                        children = [
                            dcc.Graph(id = 'Sentiment_Bar',
                            config={'displayModeBar': False},
                            animate =True,
                            figure = fig_bar
                                )
                            ]
                        ),                       
        ]),

    ])


# Callback for timeseries price
@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure
##Callback for positive/negative/neutral line graph
@app.callback(
    Output('pos_neg_graph','figure'),
    [Input('Sentimentselector','value')]
)

def update_graph_sentiment(selected_dropdown_value):
    dff = pos_df
    dff.index = pd.to_datetime(dff['created_at'])
    sentiment = px.line(
        data_frame=dff,
        x = dff.index,
        y = selected_dropdown_value

    )

    sentiment.update_layout(
                colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                template='plotly_dark',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                margin={'b': 15},
                hovermode='x',
                autosize=True,
                title={'text': 'Number of Tweets', 'font': {'color': 'white'}, 'x': 0.5},
                xaxis_title="Date",
                yaxis_title="Count",
    )
    

    return (sentiment)





if __name__ == '__main__':
    app.run_server(debug=True)
