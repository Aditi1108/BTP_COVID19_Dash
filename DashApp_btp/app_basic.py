import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import plotly.express as px

import pandas as pd
from dash.dependencies import Input, Output
import datetime

# Load data
#df = pd.read_csv('data/stockdata2.csv', index_col=0, parse_dates=True)
#df.index = pd.to_datetime(df['Date'])
senti_df = pd.read_csv('data/Number_emotion.csv')
mask_df = pd.read_excel('data/MaskData.xlsx')

Pos_df = pd.read_excel('data/Data.xlsx')
# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


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
##Table for pie chart of Masks
#labels_pie = ['Store','Home','Leisure','Public Places','Work Places']
#values_pie = [mask_df[Mask='yes',Place='Store'].sum(),mask_df[Mask='yes',Place='Home'].sum(),mask_df[Mask='yes',Place='Leisure'].sum(),mask_df[Mask='yes',Place='Public Places'].sum(),mask_df[Mask='yes',Place='Work Places'].sum()]
#fig_pie = go.Figure(data=[go.Pie(labels=labels_pie, values=values_pie)])
#fig_pie.update_layout(
 #               colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
  #             paper_bgcolor='rgba(0, 0, 0, 0)',
   #             plot_bgcolor='rgba(0, 0, 0, 0)',
    #            margin={'t': 50},
     #           hovermode='x',
      #          height = 300,
       #         #autosize=True,
        #        title={'text': 'Mask images of recorded Tweets', 'font': {'color': 'white'}, 'x': 0.5},
         #       #xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
#)

app.layout =html.Div(
            children=[
                html.Div(className = 'row heading',
                children = [
                    html.H1('VISUALISATION DASHBOARD',
                    style ={'font-family': 'Courier New','font-size' : '31px','color':'#FFFFFF','margin-bottom' : '0px'}),
                    html.H5('SENTIMENT ANALYSIS OF COVID 19 TWEETS',
                    style ={'font-family': 'Courier New','color':'#FFFFFF','padding-top':'0px','margin-top':'0px'})
                ]),
            
        
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
        ]),
    
        
        html.Div(
            className = 'row3',
            children = [
                html.Div(
                className='four columns div-user-controls',
                children=[
                    html.H2('Total masks and non masks images per day'),
                    html.P('Pick one either mask or no mask from the dropdown below.'),
                        dcc.Dropdown(
                        id='Maskyn',
                        options=[
                            {'label': 'Mask', 'value': 'Mask'},
                            {'label': 'No Mask', 'value': 'No Mask'}
                        ],
                        value='Mask',
                        clearable=False
                        ),
                    html.P('Pick one month from the dropdown below.'),
                    dcc.Dropdown(
                    id='MonthS',
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
                    dcc.Graph(id='LinePlot2', animate=True)
            ]),
                     
                                   # html.Div(className = 'div-for-charts_small bg-grey',
                                    #    children = [
                                     #       dcc.Graph(id = 'pie_graph',
                                      #      config={'displayModeBar': False},
                                       #     animate =True,
                                       #     figure = fig_pie
                                        #    )],
                    
                                        #),
                                   
               # ]),
                    
            html.Div(className = 'four columns div-for-charts bg-grey',
                children = [
                    dcc.Graph(id = 'Sentiment_Bar',
                    config={'displayModeBar': False},
                    animate =True,
                    figure = fig_bar
                    )
                    ]
                )                    
                ]
)
            ])


# Callback for timeseries price
#  plot_bgcolor='rgb(10,10,10)'                
mapVal = {'March' : 3,'April' : 4,'May' : 5}


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
#trying for mask graph
@app.callback(Output('LinePlot2','figure'),
              [Input('MonthS', 'value'),Input('Maskyn', 'value')])
def update_lineplot2(value):
    df = mask_df[pd.to_datetime(mask_df['Date']).dt.month == mapVal[value]]
    df = df.groupby(['Date', 'Place'], as_index = False, sort = True).aggregate({'Mask': 'sum'})
    linefig = px.line(df, x="Date", y="Mask", color='Place', color_discrete_map={
        "Store": "red", "Home": "green", "Leisure": "blue", "Public Spaces": "yellow", "Working Places": "orange"})
    linefig.update_xaxes(showgrid=False, zeroline=False)
    linefig.update_yaxes(showgrid=False, zeroline=False)
    
    date = datetime.datetime(2020, mapVal[value], 1)
    previous_Date = date - datetime.timedelta(days=1)
    linefig.update_layout(xaxis_range=[previous_Date,
                               datetime.datetime(2020, mapVal[value] + 1, 1)])
    colors = {
        'background': '#31302F',
        'text': '#FFFFFF'
    }

    linefig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        bargap=0.22
        )
    return linefig


if __name__ == '__main__':
    app.run_server(debug=True)
