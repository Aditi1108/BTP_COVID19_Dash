import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go

import plotly.express as px

import pandas as pd
from dash.dependencies import Input, Output
import datetime

# Load data
#df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
#df.index = pd.to_datetime(df['Date'])
senti_df = pd.read_csv('data/Number_emotion.csv')
pos_df = pd.read_csv('data/pos_neg.csv')

Pos_df = pd.read_excel('data/Data.xlsx')
# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


# def get_options(list_stocks):
#     dict_list = []
#     for i in list_stocks:
#         dict_list.append({'label': i, 'value': i})

#     return dict_list

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
        html.Div(
            children=[
                html.Div(className = 'row heading',
                children = [
                    html.H1('VISUALISATION DASHBOARD',
                    style ={'font-family': 'Courier New','font-size' : '31px','color':'#FFFFFF','margin-bottom' : '0px'}),
                    html.H5('SENTIMENT ANALYSIS OF COVID 19 TWEETS',
                    style ={'font-family': 'Courier New','color':'#FFFFFF','padding-top':'0px','margin-top':'0px'})
                ])
            ]
        ),
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('DASH - STOCK PRICES'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                     dcc.Dropdown(
                                    id='Emotion',
                                    options=[
                                        {'label': 'Positive', 'value': 'Positive'},
                                        {'label': 'Negative', 'value': 'Negative'}
                                    ],
                                    value='Positive'
                                ),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 dcc.Dropdown(
                                    id='Month',
                                    options=[
                                        {'label': 'March', 'value': 'March'},
                                        {'label': 'April', 'value': 'April'},
                                        {'label': 'May', 'value': 'May'}
                                    ],
                                    value='March'
                                )
                                
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                  #  config={'displayModeBar': False}, animate=True
                                 dcc.Graph(id='BarPlot', animate=True)
                             ])
                 ]),                            
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
                           
        html.Div(
            children=[
                html.Div(className = 'row',
                children = [
                    
                ])
            ]
        ), 
        ]
        ),
                    html.Div(className = 'four columns div-for-charts bg-grey',
                        children = [
                            dcc.Graph(id = 'Sentiment_Bar',
                            config={'displayModeBar': False},
                            animate =True,
                            figure = fig_bar
                                )
                            ]
                        ),                       
        

    ])

mapVal = {'March' : 3, 'April' : 4, 'May' : 5}
# Callback for timeseries price
@app.callback(Output('BarPlot', 'figure'),
              [Input('Month', 'value'),Input('Emotion', 'value')])
def update_graph(value,emo):
    df = Pos_df[Pos_df['Sentiment'] == emo]
    print(df.head())
    df = df[pd.to_datetime(df['Date']).dt.month == mapVal[value ]]
    df = df.groupby(['Date','Country'], as_index = False, sort = True).aggregate({'Frequency': 'sum'})
    # df = df.sort_values("Frequency", ascending=True)
    # print("Helllo")
    # df.apply(lambda x: x.sort_values(['Count'], ascending=True))
    # df = df.groupby(['Count'], sort = False).apply(lambda x: x.sort_values(['Count'], ascending=True))
    # print("Hiii \n")
    # print(df.head(4))
    fig = px.bar(df, x="Date", y="Frequency", color="Country", title="Plot")
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
