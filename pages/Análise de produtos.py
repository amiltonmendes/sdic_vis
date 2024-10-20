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
def get_data_cnae_scn_potec():
    cnae = pd.read_csv('./cnae_tabela_completa.csv',dtype={'classe_sdv' : str},sep=';').rename(columns={'Classe': 'classe','Descrição da classe':'classe_desc'})[['classe','classe_desc','classe_sdv']]
    mapeamento_cnae = pd.read_csv('mapeamento_scn_cnae_final.csv',dtype={'cnae_4d' : str,'Ativ_Divulg.' : str}).rename(columns={'Ativ_Divulg.' : 'cod_atividade','cnae_4d' : 'classe_sdv'})

    potec = pd.read_csv('matrix_potec.csv').rename(columns={'cnae_2' : 'classe_sdv'})
    potec['classe_sdv'] = potec['classe_sdv'].astype(int)
    potec['classe_sdv'] = potec['classe_sdv'].apply(str)
    potec['classe_sdv'] = potec['classe_sdv'].str.pad(5,'left','0')
    potec['classe_sdv'] = potec['classe_sdv'].str[0:4]
    potec = potec[['ano','classe_sdv','Engenheiros','Pesquisadores','Profissionais Científicos','Total Técnicos','Total Contratados']]
    potec['ano'] = potec['ano'].astype(int)

    potec = potec.merge(mapeamento_cnae,on='classe_sdv')

    potec = potec.groupby(['ano','cod_atividade'])[['Engenheiros','Pesquisadores','Profissionais Científicos','Total Técnicos','Total Contratados']].sum().reset_index()
    potec['potec'] = potec['Total Técnicos']/potec['Total Contratados']
    cnae = cnae.merge(mapeamento_cnae,on='classe_sdv')

    return potec,cnae


@st.cache_data
def get_data_scn(multiplicador_2015):
    if multiplicador_2015:
        ligacao = pd.read_csv('./indice_ligacao.csv',dtype={'cod_atividade' : str})
    else:
        ligacao = pd.read_csv('./indice_ligacao_2019.csv',dtype={'cod_atividade' : str})

    multiplicador_emprego = pd.read_csv('./vetor_gerador_emprego.csv',dtype={'cod_atividade' : str})
    remuneracao_scn = pd.read_csv('./remuneracao_media_scn.csv')

    remuneracao_scn = remuneracao_scn.stack().reset_index().drop('level_0',axis=1).rename(columns={'level_1' : 'cod_atividade', 0 : 'remuneracao_media'})
    remuneracao_scn.cod_atividade=remuneracao_scn.cod_atividade.apply(str)
    remuneracao_scn.cod_atividade = remuneracao_scn.cod_atividade.str.pad(4,'left','0')
    desc_atividade = pd.read_csv('./atividades_contas_nacionais.tsv',sep='\t',dtype={'cod_atividade' : str})
    remuneracao_scn = remuneracao_scn.merge(desc_atividade,on='cod_atividade',how='left')


    ligacao = ligacao.merge(desc_atividade,on='cod_atividade')

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
    multiplicador_2015 = st.checkbox('Utilizar os multiplicadores de 2015? ( Alternativamente serão utilizados os multiplicadores de 2019)')
    mapeamento_scn = get_data_mapeamento_sh4_scn().query('sh4=="'+select[1:5]+'"')
    if mapeamento_scn.empty:
        st.warning('Não foi possível mapear esse SH4 para uma atividade do sistema de contas nacionais. Favor entrar em contato com amilton.lobo@mdic.gov.br e indicar o código com problema.', icon="⚠️")
        st.stop()
    st.markdown("A posição de código <b>"+select[1:5]+"</b> foi mapeada para o setor do sistema de contas nacionais <b>"+mapeamento_scn['cod_atividade'].values[0]+" - "+mapeamento_scn['desc_atividade'].values[0]+"</b>",unsafe_allow_html=True)
    ligacao,multiplicador,remuneracao = get_data_scn(multiplicador_2015)
    multiplicador = multiplicador.merge(mapeamento_scn,on='cod_atividade')

    st.markdown("O multiplicador simples de emprego desse setor é <b>{}</b>, ou seja, cada R$ 1.000.000 ( um milhão ) de aumento na demanda desse setor gera uma quantidade de empregos igual a <b>{}</b> emprego(s).".format(comma_num(multiplicador['multiplicador_emprego'].values[0],':.10f'),comma_num(multiplicador['multiplicador_emprego'].values[0],':.3f')),unsafe_allow_html=True)

    ligacao_ = ligacao.merge(mapeamento_scn,on='cod_atividade')
    if (ligacao_['ligacao_frente'].values[0] > 1) & (ligacao_['ligacao_tras'].values[0] > 1):
        setor_chave = ' chave'
    else:
        setor_chave = ' não chave'
    st.markdown("Além disso, considerando que esse setor possui o índice de ligação para frente igual a <b>{}</b>, e o índice de ligação para trás igual a <b>{}</b>, esse setor é considerado um <b>setor {}</b>.".format(comma_num(ligacao_['ligacao_frente'].values[0],':.3f'),comma_num(ligacao_['ligacao_tras'].values[0],':.3f'),setor_chave),unsafe_allow_html=True)

    media_total = remuneracao[remuneracao['cod_atividade']=='total']
    remuneracao = remuneracao[remuneracao['cod_atividade']!='total']

    remuneracao=remuneracao.sort_values(by='cod_atividade')


    remuneracao['color']='lightblue'
    remuneracao.loc[remuneracao['cod_atividade'] == mapeamento_scn['cod_atividade'].values[0],'color']='red'
    
    

    
    fig = go.Figure()
    fig.add_scatter(
        x=remuneracao.sort_values(by='cod_atividade')['cod_atividade'],
        y=remuneracao.sort_values(by='cod_atividade')['remuneracao_media'],
        mode='markers',
        marker={'color': 'lightblue'},
        hovertemplate =
            '%{x}'+
            ' %{text}'+
            '<br>Remuneração média: R$ %{y:.2f}<br>',
        showlegend=False,
        text = remuneracao.sort_values(by='cod_atividade')['desc_atividade'],
        )
    fig.add_scatter(
        x=remuneracao[remuneracao['color']=='red'].sort_values(by='cod_atividade')['cod_atividade'],
        y=remuneracao[remuneracao['color']=='red'].sort_values(by='cod_atividade')['remuneracao_media'],
        mode='markers',
        marker={'color': 'red','symbol' : 'x'},
        name='Setor analisado',
        hovertemplate =
            '%{x}'+
            ' %{text}'+
            '<br>Remuneração média: R$ %{y:.2f}<br>',
        text = remuneracao[remuneracao['color']=='red'].sort_values(by='cod_atividade')['desc_atividade'],
        )

    fig.add_scatter(mode='lines',
                    x=[min(remuneracao['cod_atividade']),max(remuneracao['cod_atividade'])],
                    y=[media_total['remuneracao_media'].values[0],media_total['remuneracao_media'].values[0]],
                    line_width=0.8, line_color="red",
                    name='Remuneração média',showlegend=True,
                            hovertemplate = 'Remuneração média: R$ %{y:.2f}',
                    hoverinfo='skip'
)

    fig.update_layout(
        xaxis = dict(
            nticks=5,
        )
    )   
    fig.update_layout(template='plotly_dark',title="Remuneração média anual por setor do SCN",xaxis_title='Setor do SCN',yaxis_title='Remuneração média anual')
    fig.update_layout(separators = ',.')


    row = st.columns([1,1])

    row[0].plotly_chart(fig,use_container_width=True)

    ligacao['color']='lightblue'
    ligacao.loc[ligacao['cod_atividade'] == mapeamento_scn['cod_atividade'].values[0],'color']='red'
    figure = go.Figure()
    
    figure.add_shape(type="rect",
        x0=0.25, y0=0.30, x1=1, y1=1,
        line=dict(
            color="RoyalBlue",
            width=0,
        ),
        fillcolor="gray",
        opacity=0.2,
    )

    figure.add_trace(go.Scatter(
        x=[0.62,0.62,2.5,2.5],
        y=[0.40,1.6,0.40,1.6],
        text=["Baixo<br>encadeamento",'Alto encadeamento<br> para trás','Alto encadeamento para frente','Alto encadeamento para trás e para frente'],
        mode="text",
        hoverinfo='skip',
        showlegend=False
    ))

    figure.add_shape(type="rect",
        x0=0.25, y0=1, x1=1.0, y1=1.7,
        line=dict(
            color="RoyalBlue",
            width=0,
        ),
        fillcolor="lightblue",
        opacity=0.3,
    )

    figure.add_shape(type="rect",
        x0=1, y0=0.3, x1=4.0, y1=1,
        line=dict(
            color="RoyalBlue",
            width=0,
        ),
        fillcolor="lightblue",
        opacity=0.3,
    )
    figure.add_shape(type="rect",
        x0=1, y0=1, x1=4.0, y1=1.7,
        line=dict(
            color="RoyalBlue",
            width=0,
        ),
        fillcolor="lightgreen",
        opacity=0.3,
    )


    figure.add_scatter(
        x=ligacao[ligacao['color']=='lightblue']['ligacao_frente'],
        y=ligacao[ligacao['color']=='lightblue']['ligacao_tras'],
        mode='markers',
        name='',
        marker={'color': 'lightblue'},
        hovertemplate = '%{text}<br>'
            'ligação para frente %{x}<br>'+
            'ligação para trás %{y}',
        text = ligacao['desc_atividade'],
        showlegend=False       
        )
    figure.add_scatter(
        x=ligacao[ligacao['color']=='red']['ligacao_frente'],
        y=ligacao[ligacao['color']=='red']['ligacao_tras'],
        mode='markers',
        marker={'color': 'red','symbol' : 'x'},
        name='Setor analisado',
        hovertemplate = '%{text}<br>'
            'ligação para frente %{x}<br>'+
            'ligação para trás %{y}',
        text = ligacao['desc_atividade']        
        )
    figure.update_layout(legend={'title_text':''})

    figure.update_layout(template='plotly_dark',title="Índice de ligação para frente e para trás dos setores do SCN",xaxis_title='Índice de ligação para frente',yaxis_title='Índice de ligação para trás')
    #figure = figure.add_trace(go.Scatter(x=[0,1,1,0], y=[0,0,1,1], fill="toself",line_width=0))
    

    row[1].plotly_chart(figure,use_container_width=True)



    row = st.columns([1,1])
    potec,cnae = get_data_cnae_scn_potec()
    potec = potec[potec['cod_atividade'] == mapeamento_scn['cod_atividade'].values[0]]
    cnae = cnae[cnae['cod_atividade'] == mapeamento_scn['cod_atividade'].values[0]]
    
    ticktext = [f"{t:.2f}" for t in  potec['potec']]

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=potec["ano"], y=potec["potec"], text=ticktext,
            hovertemplate ='Ano: %{x}<br>'+
            'Potec: %{y:.3f}',
            name=''))


    fig.update_yaxes(tickformat=".2s")  
    fig.update_layout(template='plotly_dark',title="Índice Potec por ano",xaxis_title='Ano',yaxis_title='Pessoal ocupado técnico')


    row[0].plotly_chart(fig,use_container_width=True)

    row[1].markdown('<b>Códigos Cnae mapeados para conta nacional '+mapeamento_scn['cod_atividade'].values[0],unsafe_allow_html=True)
    row[1].data_editor(cnae[['classe','classe_desc']],
            column_config={
                    "classe": st.column_config.TextColumn(
                    "Classe Cnae 2.0",
                    help="Classe Cnae 2.0",
                    default="st.",
                    max_chars=50,
                    disabled=True,
                ),
                    "classe_desc": st.column_config.TextColumn(
                    "Descrição da classe",
                    help="Descrição da classe Cnae 2.0",
                    default="st.",
                    max_chars=50,
                    disabled=True,
                )

            },
    hide_index=True,   )

