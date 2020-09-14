import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import datetime

# Load data
Pos_df = pd.read_excel('data/Data.xlsx')
# print(df.head())  
# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


# def get_options(list_stocks):
#     dict_list = []
#     for i in list_stocks:
#         dict_list.append({'label': i, 'value': i})

#     return dict_list



app.layout = html.Div(
    children=[
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
                                #  ,
                                #  html.Div(
                                #      className='div-for-dropdown',
                                #      children=[
                                #          dcc.Dropdown(id='stockselector', options=get_options(df['stock'].unique()),
                                #                       multi=False, value=[df['stock'].sort_values()[0]],
                                #                       style={'backgroundColor': '#1E1E1E'},
                                #                       className='stockselector'
                                #                       ),
                                #      ],
                                #      style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                #  config={'displayModeBar': False}, animate=True
                                 dcc.Graph(id='BarPlot', animate=True)
                             ])
                              ])
        ]

)

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
#     trace1 = []
#     df_sub = df
#     for stock in selected_dropdown_value:
#         trace1.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
#                                  y=df_sub[df_sub['stock'] == stock]['value'],
#                                  mode='lines',
#                                  opacity=0.7,
#                                  name=stock,
#                                  textposition='bottom center'))
#     traces = [trace1]
#     data = [val for sublist in traces for val in sublist]
#     figure = {'data': data,
#               'layout': go.Layout(
#                   colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
#                   template='plotly_dark',
#                   paper_bgcolor='rgba(0, 0, 0, 0)',
#                   plot_bgcolor='rgba(0, 0, 0, 0)',
#                   margin={'b': 15},
#                   hovermode='x',
#                   autosize=True,
#                   title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
#                   xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
#               ),

#               }

#     return figure


if __name__ == '__main__':
    app.run_server(debug=True)
