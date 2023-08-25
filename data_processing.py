# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:25:15 2023

@author: Cristofer Costa
"""

import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go

'''
   Reading girls data
'''
birth = pd.Timestamp('2022-10-16')
with open("DB_Sofia.json", "r", encoding="utf8") as file:
    DB_sofia = json.load(file)
with open("DB_Maria.json", "r", encoding="utf8") as file:
    DB_maria = json.load(file)
    
sofia = pd.DataFrame.from_dict(DB_sofia,
                               orient='index')
maria = pd.DataFrame.from_dict(DB_maria,
                               orient='index')
'''
   Binding indexes for Sofia and Maria DB
   The indexes (date of doctors visit) is read as datetime 
   and then converted to timedelta from birth datein months
   (since the reference tables are indexed in months).
'''
gar_index = pd.to_datetime(sofia.index)
gar_delta_index = (gar_index - gar_index[-1])/np.timedelta64(1, 'M')

# Appling the new index
sofia.index = gar_delta_index
maria.index = gar_delta_index

'''
   Reading reference data
   source: https://www.who.int/tools/child-growth-standards/standards/weight-for-age
'''
source = dict()

# Girls table- Weight-for-age: Birth to 5 years (z-scores)
source['wfa_z'] = pd.read_excel('ref/wfa_girls_0-to-5-years_zscores.xlsx',
                                index_col=0)

# Girls table- Head circumference for age: Birth to 5 years (z-scores)
source['hcfa_z'] = pd.read_excel('ref/hcfa-girls-0-5-zscores.xlsx',
                                 index_col=0)

# Girls table- Length-for-age: Birth to 2 years (z-scores)
source['lfa_birth_z'] = pd.read_excel('ref/lhfa_girls_0-to-2-years_zscores.xlsx',
                                      index_col=0)

# Binding index in months delta and data from birth
source_index = {i : birth + i * pd.DateOffset(months=1)
                   for i in source['wfa_z'].index}


def plot_df(df, description, months_to_plot = 12):
    '''
       This function plots the curves from a reference and
       the values of each person.

    Parameters
    ----------
    df : Pandas DataFrame
        Reference curves.
    description: str
        Name of the column from the girl data to plot
    months_to_plot : Int, optional
        x axis in months. The default is 12.

    Returns
    -------
    plotly.graph_objects.Figure

    '''
    fig = go.Figure()
    
    # Adding reference curves
    fig.add_scatter(x=df.index,
                    y=df.SD3neg.loc[:months_to_plot].values,
                    mode='lines',
                    name='-3',
                    line={'color':'rgba(241, 148, 138, 0.5)'},
                    showlegend=False)
    fig.add_annotation(x=months_to_plot,
                       y=df.SD3neg.loc[months_to_plot],
                       text="-3",
                       showarrow=False)
    fig.add_scatter(x=df.index,
                    y=df.SD3.loc[:months_to_plot].values,
                    mode='lines',
                    name='3',
                    line={'color':'rgba(241, 148, 138, 0.5)'},
                    showlegend=False)
    fig.add_annotation(x=months_to_plot,
                       y=df.SD3.loc[months_to_plot],
                       text="3",
                       showarrow=False)
    fig.add_scatter(x=df.index,
                    y=df.SD2neg.loc[:months_to_plot].values,
                    mode='lines',
                    name='-2',
                    line={'color':'rgba(52, 152, 219, 0.5)'},
                    showlegend=False)
    fig.add_annotation(x=months_to_plot,
                       y=df.SD2neg.loc[months_to_plot],
                       text="-2",
                       showarrow=False)
    fig.add_scatter(x=df.index,
                    y=df.SD2.loc[:months_to_plot].values,
                    mode='lines',
                    name='2',
                    line={'color':'rgba(52, 152, 219, 0.5)'},
                    showlegend=False)
    fig.add_annotation(x=months_to_plot,
                       y=df.SD2.loc[months_to_plot],
                       text="2",
                       showarrow=False)
    fig.add_scatter(x=df.index,
                    y=df.SD0.loc[:months_to_plot].values,
                    mode='lines',
                    name='0',
                    line={'color':'rgba(26, 188, 156, 0.5)'},
                    showlegend=False)
    fig.add_annotation(x=months_to_plot,
                       y=df.SD0.loc[months_to_plot],
                       text="0",
                       showarrow=False)
    
    legend = {'Peso' : 'Peso em [kg]',
              'Perímetro Cefálico' : 'Perimetro Cefalico [cm]',
              'Estatura' : 'Estatura [cm]'}
    
    # Girls data
    fig.add_scatter(x=sofia.index,
                    y=sofia[description].values,
                    mode='markers',
                    name='Sofia',
                    marker=dict(size=10))
    fig.add_scatter(x=maria.index,
                    y=maria[description].values,
                    mode='markers',
                    name='Maria',
                    marker=dict(size=10))

    fig.update_layout(autosize=False,
                      width=800,
                      height=600,
                      title=description,
                      title_x=0.5,
                      xaxis=dict(title_text="Meses"),
                      yaxis=dict(title_text=legend[description]),
                      legend=dict(yanchor="top",
                                  xanchor="left",
                                  y=0.98,
                                  x=0.01))
    if __name__ != '__main__':
        fig.show()
    else:
        return fig
    
    
if __name__ == '__main__':
    import plotly.io as pio
    with open('template.html', 'r', encoding="utf8") as html:
        file = html.read()
    
    for i,j in zip(source.keys(),
                   ['Peso', 'Perímetro Cefálico', 'Estatura']):
        chart = plot_df(source[i], j)
        json_file = pio.to_json(chart)
        str_data = json.dumps(json.loads(json_file)['data'])
        str_layout = json.dumps(json.loads(json_file)['layout'])
        file = file.replace(j.upper() + '_DATA', str_data)
        file = file.replace(j.upper() + '_LAYOUT', str_layout)
        
    with open('index.html', 'w') as html:
        html.write(file)