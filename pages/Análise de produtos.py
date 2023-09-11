"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json


##TODO indicador da américa do sul

st.set_page_config(layout="wide")

@st.cache_data
def get_data_export():
    return pd.read_csv('./data_origens_exp.csv')

@st.cache_data
def get_data_import():
    return pd.read_csv('./data_destinos_imp.csv')


@st.cache_data
def get_data_polygons():
    with urlopen('https://datahub.io/core/geo-countries/r/countries.geojson') as response:
        countries = json.load(response)
        return countries


if 'df_plot' not in st.session_state:
    st.write('Preencha os parâmetros desejados no ranking de parâmetros antes de acessar a página de análise')      
    st.stop()
df_plot = st.session_state['df_plot']
df_plot = df_plot.sort_values(by='Rank',ascending=True)
#df_plot['Rank'] = df_plot['Rank'].apply(int)
#df_plot['RankDesc'] = df_plot['Rank'].apply(str) + ' ' +df_plot['Descrição']
df_plot['SH_Desc'] = '(' +df_plot[' Código HS 2007'].apply(str) + ') ' +df_plot['Descrição'].str.slice(0,100)

select = st.selectbox("Selecione o produto a ser analisado: ", df_plot['SH_Desc'])



Origens, Destinos = st.tabs(["1. Origens", "2. Destinos"])
df = get_data_export()
df = df.query('hs_product_code=="'+select[1:5]+'"')

with Origens:
    df_exp = get_data_export().query('hs_product_code=="'+select[1:5]+'"').query('year==2021')
    df_exp['%'] = df_exp['%']*100

    #df_exp = df_exp.rename(columns={'location_code' : 'País', 'export_value' : 'Valor exportado', '%' : 'Participação na exportação'})
    countries = get_data_polygons()
    fig = px.choropleth_mapbox(df_exp, geojson=countries, locations='location_code', color='%',hover_name="location_code", hover_data=["%", "export_value","cummul"],
                            color_continuous_scale="Viridis",
                            featureidkey="properties.ISO_A3",
                            #range_color=(0, 30),
                            mapbox_style="carto-positron",
                            zoom=1, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5,
                            labels={'%' : 'Participação na exportação' , 'location_code' : 'País Iso3','export_value' : 'Valor exportado',"cummul" : 'Percentual acumulado'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    

with Destinos:
    df_imp = get_data_import().query('hs_product_code=="'+select[1:5]+'"').query('year==2021')
    df_imp['%'] = df_imp['%']*100

    countries = get_data_polygons()
    fig = px.choropleth_mapbox(df_imp, geojson=countries, locations='location_code', color='%',hover_name="location_code", hover_data=["%", "import_value","cummul"],
                            color_continuous_scale="Viridis",
                            featureidkey="properties.ISO_A3",
                            #range_color=(0, 10),
                            mapbox_style="carto-positron",
                            zoom=1, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5,
                            labels={'%' : 'Participação na importação' , 'location_code' : 'País Iso3','import_value' : 'Valor importado',"cummul" : 'Percentual acumulado'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
