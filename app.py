import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os
from dash.dependencies import Input, Output

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
csv_fnames = [d for d in os.listdir(".") if d.startswith("00000")]
csv_fnames.sort(key= lambda x: x.split("_")[3])
print (csv_fnames)
graph_list = []

min_date = pd.datetime(year=2010,month=4,day=21)
max_date = pd.datetime(year=2018,month=6,day=17)

print (min_date,max_date)

for fname in csv_fnames:
#    df = pd.read_csv(fname,names=["Date","Tavg","Tmax","Tmin","Havg","Hmin","Hmax","prec","opstina","mesto","usev"],index_col="Date")[["Tavg","opstina","mesto","usev"]]
    df = pd.read_csv(fname,usecols=[0,1],index_col="Date",converters={"Date":pd.to_datetime})
    df.columns = ["Tavg"]
    graph_list.append(dcc.Graph(id=fname,
              figure= {
                  'data': [
                      {'x' : df.index,'y':df.Tavg, 'type': 'line','name':'Tavg'}
                  ],
                  'layout': {
                      'title':"Average temperature {}".format(fname.split("_")[0:4]),
                      'yaxis':{'title': "T avg (celsius)"},
                      'xaxis':{'range':[min_date,max_date]}
#                               'rangeselector':{ 'buttons':[{'count':1,'label':'1m','step':'month','stepmode':'backward'},{'count':6,'label':'6m','step':'month','stepmode':'backward'},{'step':'all'}]},
#                               'rangeslider':{'visible':True}

                  }
              })
    )

    
childrenn = [html.H1("PIS podaci"),
                                   dcc.Input (id="input", value = "", type="text"),
                                   html.Div(id="graphs",children=graph_list)]

app.layout = html.Div (children=childrenn)



#@app.callback(
#    Output(component_id="output", component_property="children"),
#    [Input(component_id='input', component_property="value")])
#def update_value(input_data):
#    return "Input : {}".format(input_data)
                                   
if __name__ == "__main__":
    app.run_server(debug=True)
                                   
