# Pt4 fetches stored tweets from SQLite and analyses them and visualises using Dash.
# dr stacey
# cd to the directory where this script 'lives' and run it from there.

import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd

#popular topics: google, olympics, trump, gun, usa

app = dash.Dash(__name__)
app.layout = html.Div(
    [   html.H2('Live Twitter Sentiment Analysis on term:'),
        dcc.Input(id='sentiment_term', value='', type='text'), #this enables you to input a search term/filter which then automatically updates the graph in real time.
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

#all the dash logic moved into callback beause we want it to be live, not static. 
@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='sentiment_term', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(sentiment_term): #decorator function.
    try:
        conn = sqlite3.connect('twitter_sentiment.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn ,params=('%' + sentiment_term + '%',)) #try changing/playing the limit to see the effect on the graph
        df.sort_values('unix', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean() #try changing this too - smoothens ??? the data
        
        #tidy up the date! 
        df['date'] = pd.to_datetime(df['unix'],unit='ms') #readable date!
        df.set_index('date', inplace=True)
        
        #df = df.resample('1min').mean() #force resample, but becomes less responsive. #leave for now
        df.dropna(inplace=True)

        #X = df.unix.values[-100:]
        X = df.index #update the X
        Y = df.sentiment_smoothed.values #try changing this value too
        #Y = df.sentiment_smoothed.values[-1000:] #try changing this value too

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),)}
#so this is how the real time sentiment analysis is achieved
    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')


if __name__ == '__main__':
    app.run_server(debug=True)

#note: the start date for X axis is determined by when you started collecting the tweets

#optinal: try incorporating this into CODA, e.g. could take the ticker and search for that
