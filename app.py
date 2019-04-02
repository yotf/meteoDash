import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
csv_fnames = [d for d in os.listdir(".") if d.startswith("00000")]

graph_list = []
for fname in csv_fnames:
    print (fname)
#    df = pd.read_csv(fname,names=["Date","Tavg","Tmax","Tmin","Havg","Hmin","Hmax","prec","opstina","mesto","usev"],index_col="Date")[["Tavg","opstina","mesto","usev"]]
    df = pd.read_csv(fname,usecols=[0,1],index_col="Date",names=["Date","Tavg"])
    graph_list.append(dcc.Graph(id=fname,
              figure= {
                  'data': [
                      {'x' : df.index,'y':df.Tavg, 'type': 'line','name':'Tavg'}
                  ],
                  'layout': {
                      'title':"Average temperature {}".format(fname.split("_")[0:4])
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
                                   
