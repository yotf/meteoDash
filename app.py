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

graph_config = {"toImageButtonOptions":{"width":1500,"height":600,"scale":1}}#,"modeBarButtonsToAdd":["sendDataToCloud"]}

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
    def make_graphs_for_sort(sorta,vrednost):
        def read_dataframes_for_sort(sorta,koje):
            """Ucitava ih sve u listu iz kojih ce se posle praviti grafici"""
            graph_content_list = []
            dfs = dict()
            po_sorti = [fname for fname in pickle_fnames[koje] if sorta in fname and not sorta + " Ogled" in fname]
            for fname in po_sorti:
                df = pd.read_pickle(fname)
                graph_content_list.append({"id":fname,"x":df.index,"y":df[vrednost]})
            return graph_content_list
        def determine_max_min_2d(list_of_lists):
            """Gets list of lists and determines min and max"""
            min_date = None
            max_date = None
            for ls in list_of_lists:
                min_date = ls.min() if not min_date else (ls.min() if ls.min() <min_date else min_date)
                max_date = ls.max() if not max_date else (ls.max() if ls.max() > max_date else max_date)
            return max_date,min_date
        graphlist_sorta=[]
        start = timer()
        graph_content_list = read_dataframes_for_sort(sorta,koje)
        end = timer()
        print ("proslo vremena na citanje %s" %(end-start))
        start = timer()
        dates = [item['x'] for item in graph_content_list]
        values = [item['y'] for item in graph_content_list]
        maxd,mind = determine_max_min_2d(dates)
        maxv,minv = determine_max_min_2d(values)
        print (maxd,mind)
        print (minv,maxv)
        for graph_content in graph_content_list:
            graph_data = [{'x' : graph_content["x"],'y':graph_content["y"], 'type': "line", "mode": tipovi_grafika[vrednost],'name':vrednost},
                      {'x' : graph_content["x"],'y':graph_content["y"].rolling(10).mean(),"error_y": {"array": graph_content["y"].rolling(10).std(), "visible":True,'width':0}, 'name':"rolling average"}] if koje=="average" else [{'x' : graph_content["x"],'y':graph_content["y"], 'type': "line", "mode": tipovi_grafika[vrednost],'name':vrednost}]
            graphlist_sorta.append(html.Div(children=[html.Button('Details',id=graph_content["id"]),dcc.Graph(id="g"+graph_content["id"],config=graph_config,
              figure= {
                  'data': graph_data,
                  'layout': {
                      'title':{"text":"{} {}".format(vrednost,graph_content["id"].split("_")[0:6]),"font":{"size":20}},
                      'yaxis':{'title':{"text": vrednost,"font":{"size":25}},'range':[minv,maxv],'zeroline':False if vrednost=="bowen" else True,"tickfont":{"size":25}},
                      'xaxis':{'range':[mind,maxd],"tickfont":{"size":25},'dtick':30 if koje=="average" else None},
                      'legend':{'font':{"size":20}},
                      'shapes':[{'type':'line', 'y0':1,'y1':1,'x0':0,'x1':365,'line':{'width':0.8}} if vrednost=="bowen" else None]
                  }
              })]))
        end = timer()
        print ("proslo vremena na crtanje %s" %(end-start))
        return graphlist_sorta

    graphlist= []
    for sorta in sorte_list:
        print (sorta,vrednost)
        graphlist+= make_graphs_for_sort(sorta,vrednost)
    return graphlist



                                   
if __name__ == "__main__":
    app.run_server(debug=True)
                                   
