"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.colors import n_colors

import pandas as pd
from urllib.request import urlopen
import json


st.set_page_config(layout="wide")

def comma_num(n,f=''):
    return ('{'+f+'}').format(n).replace('.',',')

@st.cache_data
def get_data_export():
    retorno = pd.read_csv('./data_origens_exp.csv')
    retorno = retorno.merge(pd.read_csv('./PAIS.csv',sep=';',dtype={'CO_PAIS_ISOA3' : str})[['CO_PAIS','CO_PAIS_ISOA3','NO_PAIS']].rename(columns={'CO_PAIS_ISOA3' : 'location_code', 'NO_PAIS' : 'no_pais'}),on='location_code')
    retorno = retorno.query('CO_PAIS not in (396,873,152,786,628,278,20,151,237,25,100)')

    return retorno.sort_values(by='export_value',ascending=False)

@st.cache_data
def get_data_import():
    retorno = pd.read_csv('./data_importacoes_totais_ano_sh4.csv')
    return retorno

@st.cache_data
def get_data_mapeamento_sh4_scn():
    retorno = pd.read_csv('./mapeamento_final_sh4_scn.csv',dtype={'sh4' : str, 'atividade_scn' : str}).rename(columns={'atividade_scn' : 'cod_atividade'})
    retorno = retorno.merge(pd.read_csv('./atividades_contas_nacionais.tsv',sep='\t',dtype={'cod_atividade' : str}),on='cod_atividade')
    return retorno

@st.cache_data
def get_data_scn():
    ligacao = pd.read_csv('./indice_ligacao.csv',dtype={'cod_atividade' : str})
    multiplicador_emprego = pd.read_csv('./vetor_gerador_emprego.csv',dtype={'cod_atividade' : str})
    remuneracao_scn = pd.read_csv('./remuneracao_media_scn.csv')

    remuneracao_scn = remuneracao_scn.stack().reset_index().drop('level_0',axis=1).rename(columns={'level_1' : 'cod_atividade', 0 : 'remuneracao_media'})
    remuneracao_scn.cod_atividade=remuneracao_scn.cod_atividade.apply(str)
    remuneracao_scn.cod_atividade = remuneracao_scn.cod_atividade.str.pad(4,'left','0')
    desc_atividade = pd.read_csv('./atividades_contas_nacionais.tsv',sep='\t',dtype={'cod_atividade' : str})
    remuneracao_scn = remuneracao_scn.merge(desc_atividade,on='cod_atividade')


    return ligacao,multiplicador_emprego,remuneracao_scn



@st.cache_data
def get_data_polygons():
    with urlopen('https://datahub.io/core/geo-countries/r/countries.geojson') as response:
        countries = json.load(response)
        return countries


if 'df_plot' not in st.session_state:
    st.write('Preencha os parâmetros desejados no ranking de parâmetros antes de acessar a página de análise')      
    st.stop()
df_plot = st.session_state['df_plot']
df_plot = df_plot.sort_values(by='rank',ascending=True)
#df_plot['Rank'] = df_plot['Rank'].apply(int)
#df_plot['RankDesc'] = df_plot['Rank'].apply(str) + ' ' +df_plot['Descrição']
df_plot['sh_desc'] = '(' +df_plot['hs_product_code'].apply(str) + ') ' +df_plot['no_sh4'].str.slice(0,100)

st.markdown("Selecione o produto a ser analisado: ")
select = st.selectbox("Selecione o produto a ser analisado: ", df_plot['sh_desc'],label_visibility='collapsed')



Origens, Matriz = st.tabs(["1. Comércio Internacional", "2. Matriz de Insumo-Produto"])
df = get_data_export()
df = df.query('hs_product_code=="'+select[1:5]+'"')

with Origens:
    df_exp = get_data_export().query('hs_product_code=="'+select[1:5]+'"').query('year==2021')
    df_exp['%'] = df_exp['%']*100

    st.markdown('### Exportação')

    row = st.columns([3,1,3])

    fig = px.pie(df_exp,title='Volume de exportações por origem', values='export_value', names='no_pais',labels={'no_pais' : 'País','export_value' : 'Valor exportado'})
    fig.update_traces(texttemplate="US$ %{value:,d}")
    fig.update_layout(separators = ',.')

    row[0].plotly_chart(fig,use_container_width=True)

    fig = px.funnel(df_exp,title='Participação no comércio mundial por origem', x='%', y='no_pais',labels={'no_pais' : 'País','%' : 'Participação mundial'})
    fig.update_traces(texttemplate="%{value:,.2f}%")
    row[2].plotly_chart(fig,use_container_width=True)
    
    df_exp = get_data_export().query('hs_product_code=="'+select[1:5]+'"')
    
    fig = px.histogram(df_exp.sort_values(by=['no_pais','year','export_value']),barnorm='percent', x="year", y="export_value",labels={'no_pais' : 'País','export_value' : 'Valor exportado (US$)', 'year' : 'Ano'}, color="no_pais", title="Série histórica da participação das principais origens do produto por ano")
    fig.update_layout(yaxis_title="Exportação em US$")
    fig.update_layout(bargap=0.2)


    st.plotly_chart(fig,use_container_width=True)

    st.markdown('### Importação')
    df_imp = get_data_import().query('hs_product_code=="'+select[1:5]+'"')
    ticktext = [f"US$ {int(t // 1000000):,}M".replace(',','.') for t in  df_imp['import_value']]
    
    fig = px.line(df_imp, x="year", y="import_value", text=ticktext,labels={'year' : 'Ano','import_value' : 'Valor importado', 'text' : 'Valor'})
    fig.update_traces(textposition="bottom right")
    fig.update_layout(separators = ',.')
    #fig.update_traces(texttemplate="US$ %{value:,d}")

    st.plotly_chart(fig,use_container_width=True)

with Matriz:
    mapeamento_scn = get_data_mapeamento_sh4_scn().query('sh4=="'+select[1:5]+'"')
    if mapeamento_scn.empty:
        st.warning('Não foi possível mapear esse SH4 para uma atividade do sistema de contas nacionais. Favor entrar em contato com amilton.lobo@mdic.gov.br e indicar o código com problema.', icon="⚠️")
        st.stop()
    st.markdown("A posição de código <b>"+select[1:5]+"</b> foi mapeada para o setor do sistema de contas nacionais <b>"+mapeamento_scn['cod_atividade'].values[0]+" - "+mapeamento_scn['desc_atividade'].values[0]+"</b>",unsafe_allow_html=True)
    ligacao,multiplicador,remuneracao = get_data_scn()
    multiplicador = multiplicador.merge(mapeamento_scn,on='cod_atividade')

    st.markdown("O multiplicador simples de emprego desse setor é <b>{}</b>, ou seja, cada R$ 1.000.000 ( um milhão ) de aumento na demanda desse setor gera uma quantidade de empregos igual a <b>{}</b> emprego(s).".format(comma_num(multiplicador['multiplicador_emprego'].values[0],':.10f'),comma_num(multiplicador['multiplicador_emprego'].values[0],':.3f')),unsafe_allow_html=True)

    ligacao_ = ligacao.merge(mapeamento_scn,on='cod_atividade')
    if (ligacao_['ligacao_frente'].values[0] > 1) & (ligacao_['ligacao_tras'].values[0] > 1):
        setor_chave = ' chave'
    else:
        setor_chave = ' não chave'
    st.markdown("Além disso, considerando que esse setor possui o índice de ligação para frente igual a <b>{}</b>, e o índice de ligação para trás igual a <b>{}</b>, esse setor é considerado um <b>setor {}</b>.".format(comma_num(ligacao_['ligacao_frente'].values[0],':.3f'),comma_num(ligacao_['ligacao_tras'].values[0],':.3f'),setor_chave),unsafe_allow_html=True)

    remuneracao = remuneracao[remuneracao['cod_atividade']!='total']
    #fig = px.box(remuneracao, y="remuneracao_media", points="all",labels={'remuneracao_media' : 'Remuneração média (anual)'})
    
    remuneracao['color']='lightblue'
    remuneracao.loc[remuneracao['cod_atividade'] == mapeamento_scn['cod_atividade'].values[0],'color']='red'
    remuneracao['grafico'] = 'teste'
    
    remuneracao=remuneracao.sort_values(by='cod_atividade')

    
    fig = go.Figure()
    fig.add_scatter(
        x=remuneracao['cod_atividade'],
        y=remuneracao['remuneracao_media'],
        mode='markers',
        marker={'color': remuneracao['color']},
        hovertemplate =
            '%{x}'+
            ' %{text}'+
            '<br>Remuneração média: R$ %{y:.2f}<br>',
        text = remuneracao['desc_atividade']
        )
    fig.update_layout(template='plotly_dark',title="Remuneração média anual por setor do SCN",xaxis_title='Setor do SCN',yaxis_title='Remuneração média anual')
    fig.update_layout(separators = ',.')


    
    st.plotly_chart(fig)

    ligacao['color']='lightblue'
    ligacao.loc[ligacao['cod_atividade'] == mapeamento_scn['cod_atividade'].values[0],'color']='red'
    figure = go.Figure()
    figure.add_scatter(
        x=ligacao['ligacao_frente'],
        y=ligacao['ligacao_tras'],
        mode='markers',
        marker={'color': ligacao['color']},
        hovertemplate = '%{text}<br>'
            'ligação para frente %{x}<br>'+
            'ligação para trás %{y}',
        text = remuneracao['desc_atividade']        
        )
    figure.update_layout(template='plotly_dark',title="Índice de ligação para frente e para trás dos setores do SCN",xaxis_title='Índice de ligação para frente',yaxis_title='Índice de ligação para trás')
    figure.show()    
    st.plotly_chart(figure)

