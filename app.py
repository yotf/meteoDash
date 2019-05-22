import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os
from dash.dependencies import Input, Output, State
from collections import defaultdict
from timeit import default_timer as timer
from metpy.calc import thermo
from metpy.units import units
dataframes = defaultdict(dict)

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
pickle_fnames = dict()
pickle_fnames["hourly"] = [d for d in os.listdir(".") if d.startswith("0000") and d.endswith("_hourly.pkl")]
pickle_fnames["daily"] = [d for d in os.listdir(".") if d.startswith("0000") and d.endswith("_daily.pkl")]
pickle_fnames["average"] = [ d for d in os.listdir(".") if d.startswith("0000") and d.endswith("_AVG.pkl")]
print (pickle_fnames)
sorte = list(set([x.split("_")[3] for x in pickle_fnames["hourly"]]))

#vrednosti_stilovi = {"lcl":

sorte_traduction = {"Kruska":"Pear","Jabuka":"Apple","Jabuka Ogled":"Apple Experiment","Vinova Loza":"Grape Vine","Sljiva":"Plum","Visnja":"Sour Cherry"}
dropdown= dcc.Dropdown(id = "sorte_dropdown",
                       options=[{'label':sorte_traduction[sorta],'value':sorta} for sorta in sorte],
                       value=["Kruska"],
                       multi =True
    )

radio_ds = dcc.RadioItems(
    options=[
            {'label': 'Average Daily', 'value': 'daily'},
            {'label': 'Hourly', 'value': 'hourly'},
            {'label': 'Averaged over years',"value":"average"}

        ],
    value='hourly',
    id ="koje"
    )

options_hourly =  [{'label':"Average temperature",'value':"Tavg"},
                   {'label':"Relative humidity", "value" : "RH"},
                   {'label':"LCL", "value" :"lcl"},
                   {'label':"q", "value" :"q"},
                   {'label':"qsat", "value" :"qsat"},
                   {'label':"Precipitation", "value" :"Precipitation"},
                   {'label':"Dew Point", "value" :"dewpoint"}]


options_daily = options_hourly + [{'label':"Bowen daily", "value" :"bowen"},
                                  {'label':"Temperature Tendency daily", "value" :"tendt"},
                                  {'label':"Q Tendency daily", "value" :"tendq"},
                                  {'label':"R1", "value" :"R1"},
                                  {'label':"R2", "value" :"R2"},
                                  {'label':"Minimal daily Temperature", "value" :"Tmin"},
                                  {'label':"Maximal daily Temperature", "value" :"Tmax"}]


dropdown_vrednosti = dcc.Dropdown(id="vrednosti_drop",
                                  options =options_hourly,
                                  value="Tavg",
                                  multi=False

                                  )

tipovi_grafika = defaultdict(lambda: "lines")
tipovi_grafika["bowen"] ="markers"

    
childrenn = [html.H1("Observed Data - Vojvodina"),
                                   radio_ds,dropdown_vrednosti,dropdown,
                                   html.Div(id="graphs")]

app.layout = html.Div (children=childrenn)

@app.callback(
    Output(component_id='vrednosti_drop', component_property='options'),
    [Input(component_id='koje', component_property='value')],[State(component_id ="vrednosti_drop",component_property="options")]
)
def update_vrednosti_drop(koje,options):
    assert(koje=="daily" or koje=="hourly" or koje=="average")
    return options_hourly if koje=="hourly" else options_daily


@app.callback(
    Output(component_id='graphs', component_property='children'),
    [Input(component_id='sorte_dropdown', component_property='value'),Input(component_id='vrednosti_drop',component_property='value'),Input(component_id="koje",component_property="value")]
)
def update_output_div(sorte_list,vrednost,koje):
    graphlist = []
    def make_graphs_for_sort(sorta,vrednost):
        def read_dataframes_for_sort(sorta,koje):
            dfs = dict()
            po_sorti = [fname for fname in pickle_fnames[koje] if sorta in fname and not sorta + " Ogled" in fname]
            for fname in po_sorti:
                df = pd.read_pickle(fname)
                dfs[fname]=df
            return dfs
        min_date = None
        max_date = None
        graphlist_sorta=[]
        start = timer()
        dataframes_sorta = read_dataframes_for_sort(sorta,koje)
        end = timer()
        print ("proslo vremena na citanje %s" %(end-start))
        start = timer()
        for fname,df in dataframes_sorta.items():
            min_date = df.index[0] if not min_date else (df.index[0] if df.index[0] <min_date else min_date)
            max_date = df.index[-1] if not max_date else (df.index[-1] if df.index[-1] > max_date else max_date)
        for fname,df in dataframes_sorta.items():
            graphlist_sorta.append(dcc.Graph(id=fname,
              figure= {
                  'data': [
                      {'x' : df.index,'y':df[vrednost], 'type': "line", "mode": tipovi_grafika[vrednost],'name':vrednost}
                  ],
                  'layout': {
                      'title':"{} {}".format(vrednost,fname.split("_")[0:4]),
                      'yaxis':{'title': vrednost},
                      'xaxis':{'range':[min_date,max_date]}
                  }
              }))
        end = timer()
        print ("proslo vremena na crtanje %s" %(end-start))
        return graphlist_sorta
        
    for sorta in sorte_list:
        print (sorta,vrednost)
        graphlist+= make_graphs_for_sort(sorta,vrednost)

    print(graphlist)

    return graphlist



                                   
if __name__ == "__main__":
    app.run_server(debug=True)
                                   
