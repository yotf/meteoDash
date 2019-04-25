import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os
from dash.dependencies import Input, Output, State
from collections import defaultdict

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
csv_fnames = [d for d in os.listdir(".") if d.startswith("0000")]
csv_fnames.sort(key= lambda x: x.split("_")[3])
print (csv_fnames)
graphdict = dict()

sorte = list(set([x.split("_")[3] for x in csv_fnames]))

sorte_traduction = {"Kruska":"Pear","Jabuka":"Apple","Jabuka Ogled":"Apple Experiment","Vinova Loza":"Grape Vine","Sljiva":"Plum"}
dropdown= dcc.Dropdown(id = "sorte_dropdown",
                       options=[{'label':sorte_traduction[sorta],'value':sorta} for sorta in sorte],
                       value=["Kruska"],
                       multi =True
                       
    
    )

radio_ds = dcc.RadioItems(
    options=[
            {'label': 'Average Daily', 'value': 'daily'},
            {'label': 'Hourly', 'value': 'hourly'}

        ],
    value='hourly',
    id ="koje"
    )

dropdown_funkc = dcc.Dropdown(id="panel_dropdown",
                              options = [{'label':"Pregled satnih vrednosti",'value':"Tavg"},
                                         {'label':"Fenologija",'value':"fen"}]
                              )

#{'label':"Bowen daily", "value" :"bowen"},
#{'label':"Temperature Tendency daily", "value" :"tendt"},
#{'label':"Q Tendency daily", "value" :"tendq"}


dropdown_vrednosti = dcc.Dropdown(id="vrednosti_drop",
                                  options = [{'label':"Average temperature",'value':"Tavg"},
                                             {'label':"Relative humidity", "value" : "RH"},
                                             {'label':"LCL", "value" :"lcl"},
                                             {'label':"q", "value" :"q"},
                                             {'label':"qsat", "value" :"qsat"},
                                             {'label':"Dew Point", "value" :"dewpoint"}
                                             ],
                                  value="Tavg"
                                  )

    
childrenn = [html.H1("PIS podaci"),
                                   radio_ds,dropdown_vrednosti,dropdown,
                                   html.Div(id="graphs")]

app.layout = html.Div (children=childrenn)


@app.callback(
    Output(component_id='graphs', component_property='children'),
    [Input(component_id='sorte_dropdown', component_property='value'),Input(component_id='vrednosti_drop',component_property='value'),Input(component_id="koje",component_property="value")]
)
def update_output_div(sorte_list,vrednost,koje):
    min_date = None
    max_date = None
    graphlist = []
    for sorta in sorte_list:
        graphlist_sorta=[]
        print (sorta)
        po_sorti = [fname for fname in csv_fnames if sorta in fname]
        dataframes = dict()
        for fname in po_sorti:
            df = pd.read_csv(fname,index_col="Date",converters={"Date":pd.to_datetime})
            min_date = df.index[0] if not min_date else (df.index[0] if df.index[0] <min_date else min_date)
            max_date = df.index[-1] if not max_date else (df.index[-1] if df.index[-1] > max_date else max_date)
            dataframes[fname] =df
        for fname,df in dataframes.items():
            df = df if koje=="hourly" else df.resample('D').mean()
            graphlist_sorta.append(dcc.Graph(id=fname,
              figure= {
                  'data': [
                      {'x' : df.index,'y':df[vrednost], 'type': 'line','name':vrednost}
                  ],
                  'layout': {
                      'title':"Average temperature {}".format(fname.split("_")[0:4]),
                      'yaxis':{'title': "T avg (celsius)"},
                      'xaxis':{'range':[min_date,max_date]}
                  }
              }))

        graphdict[sorta]=graphlist_sorta
        graphlist = graphlist+ graphlist_sorta
    return graphlist


                                   
if __name__ == "__main__":
    app.run_server(debug=True)
                                   
