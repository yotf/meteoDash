import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

df = pd.read_csv('00000DAD_KI_KI_Sljiva_2016-11-01 00:00:00.csv',usecols=[0,1],index_col="Date",names=["Date","Tavg"])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div (children = [html.H1("PIS podaci"),
                                   dcc.Graph(id="example",
                                                 figure= {
                                                     'data': [
                                                         {'x' : df.index,'y':df.Tavg, 'type': 'line','name':'Tavg'}
                                                         ],
                                                      'layout': {
                                                          'title':"Average temperature""

                                                          }
                                                     })
                                                          ])
                                   
if __name__ == "__main__":
    app.run_server(debug=True)
                                   
