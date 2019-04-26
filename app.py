import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os
from dash.dependencies import Input, Output, State
from collections import defaultdict
from timeit import default_timer as timer
dataframes = defaultdict(dict)

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
pickle_fnames = [d for d in os.listdir(".") if d.startswith("0000") and d.endswith(".pkl")]
pickle_fnames.sort(key= lambda x: x.split("_")[3])
graphdict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

sorte = list(set([x.split("_")[3] for x in pickle_fnames]))

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



options_hourly =  [{'label':"Average temperature",'value':"Tavg"},
                   {'label':"Relative humidity", "value" : "RH"},
                   {'label':"LCL", "value" :"lcl"},
                   {'label':"q", "value" :"q"},
                   {'label':"qsat", "value" :"qsat"},
                   {'label':"Dew Point", "value" :"dewpoint"}]


options_daily = options_hourly + [{'label':"Bowen daily", "value" :"bowen"},
                                  {'label':"Temperature Tendency daily", "value" :"tendt"},
                                  {'label':"Q Tendency daily", "value" :"tendq"}]


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

    
childrenn = [html.H1("Observed Data - Vojvodina"),
                                   radio_ds,dropdown_vrednosti,dropdown,
                                   html.Div(id="graphs")]

app.layout = html.Div (children=childrenn)

@app.callback(
    Output(component_id='vrednosti_drop', component_property='options'),
    [Input(component_id='koje', component_property='value')],[State(component_id ="vrednosti_drop",component_property="options")]
)
def update_vrednosti_drop(koje,options):
    print(koje)
    print(options)
    assert(koje=="daily" or koje=="hourly")
    return options_daily if koje=="daily" else options_hourly


@app.callback(
    Output(component_id='graphs', component_property='children'),
    [Input(component_id='sorte_dropdown', component_property='value'),Input(component_id='vrednosti_drop',component_property='value'),Input(component_id="koje",component_property="value")]
)
def update_output_div(sorte_list,vrednost,koje):
    graphlist = []
    def make_graphs_for_sort(sorta):
        def read_dataframes_for_sort(sorta):
            dfs = dict()
            po_sorti = [fname for fname in pickle_fnames if sorta in fname and not sorta + " Ogled" in fname]
            for fname in po_sorti:
                df = pd.read_pickle(fname)
                dfs[fname]=df
            return dfs
        min_date = None
        max_date = None
        graphlist_sorta=[]
        print (sorta)
        start = timer()
        dataframes[sorta] = dataframes[sorta] if sorta in dataframes else read_dataframes_for_sort(sorta)
        end = timer()
        print ("proslo vremena na citanje %s" %(end-start))
        start = timer()

        for fname,df in dataframes[sorta].items():
            min_date = df.index[0] if not min_date else (df.index[0] if df.index[0] <min_date else min_date)
            max_date = df.index[-1] if not max_date else (df.index[-1] if df.index[-1] > max_date else max_date)
        for fname,df in dataframes[sorta].items():
            df = df if koje=="hourly" else df.resample('D').mean()
            if koje=="hourly":
                Lv = 2265.705
                Cp = 1.003
                df["tendt"] = Cp*df.Tavg.diff()/(24*3600)
                df["tendq"] = Lv*df.q.diff()/(24*3600)
                df["bowen"] = (Cp*df.Tavg.diff())/(Lv*df.q.diff())
                df.bowen[(df.bowen>5) | (df.bowen<-2)] = None
#                df["R1"] =
#                df["R2"] = 
            graphlist_sorta.append(dcc.Graph(id=fname,
              figure= {
                  'data': [
                      {'x' : df.index,'y':df[vrednost], 'type': 'line','name':vrednost}
                  ],
                  'layout': {
                      'title':"{} {}".format(vrednost,fname.split("_")[0:4]),
                      'yaxis':{'title': vrednost},
                      'xaxis':{'range':[min_date,max_date]}
                  }
              }))
        end = timer()
        print ("proslo vremena na crtanje %s" %(end-start))
        graphdict[sorta][vrednost][koje]=graphlist_sorta
        return graphlist_sorta
        
    for sorta in sorte_list:
        graphlist+= graphdict[sorta][vrednost][koje] if graphdict[sorta][vrednost][koje] else make_graphs_for_sort(sorta)

    return graphlist



                                   
if __name__ == "__main__":
    app.run_server(debug=True)
                                   
