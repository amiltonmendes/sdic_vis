"""
# My first app
Here's our first attempt at using data to create a table:
"""

import pandas as pd
import streamlit as st
import pandas as pd
import locale


st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    locale._override_localeconv = {'thousands_sep': '.'}
    retorno = pd.read_csv('./raw_indice_normalizado.csv')
    
    retorno = retorno[retorno['rca']<1]
    return retorno

df = load_data()



        

# Inicialização de sessão
if 'slider_CapacidadesAtuais' not in st.session_state:
    st.session_state['slider_CapacidadesAtuais'] = (33,66)
if 'slider_Oportunidades' not in st.session_state:
    st.session_state['slider_Oportunidades'] = (33,66)
if 'slider_Ganhos' not in st.session_state:
    st.session_state['slider_Ganhos'] = 50
if 'peso_crescimento' not in st.session_state:
    st.session_state['peso_crescimento'] = 0.25
if 'peso_importacao_global' not in st.session_state:
    st.session_state['peso_importacao_global'] = 0.25
if 'peso_importacao' not in st.session_state:
    st.session_state['peso_importacao'] = 0.25
if 'peso_dcr' not in st.session_state:
    st.session_state['peso_dcr'] = 0.25


row = st.columns([1,7])
peso_capacidade_atuais = row[0].number_input('Insert a number',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')
with row[1].expander("Capacidades atuais"):
    header = st.columns([1,1,1,2])
    #header[0].markdown('#### Capacidades Atuais')
    header[1].markdown('<div style="text-align: right;">Valor exportado: '+"{:.2f}".format(float(st.session_state['slider_CapacidadesAtuais'][0]/100))+'</div>',unsafe_allow_html=True)
    header[1].markdown('<div style="text-align: right;">Vantagem comparativa revelada: '+"{:.2f}".format(float((st.session_state['slider_CapacidadesAtuais'][1]-st.session_state['slider_CapacidadesAtuais'][0])/100))+'</div>',unsafe_allow_html=True)
    header[1].markdown('<div style="text-align: right;">Densidade do produto: '+"{:.2f}".format(float((100-st.session_state['slider_CapacidadesAtuais'][1])/100)) +'</div>',unsafe_allow_html=True)
    
    sliderCapacidades = header[3].slider('Capacidades.', 0, 100, key='slider_CapacidadesAtuais', label_visibility='hidden')

row = st.columns([1,7])
peso_oportunidaes=row[0].number_input('Oportunidades',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')
with row[1].expander("Oportunidades de mercado"):
    header = st.columns([1,1,1,1,1])
    header[1].markdown('<div style="text-align: right;">Valor importado: '+"{:.2f}".format(float(st.session_state['peso_importacao']))+'</div>',unsafe_allow_html=True)
    header[3].number_input('Importacao',min_value=0.0,max_value=1.0,key='peso_importacao',label_visibility='collapsed')

    header = st.columns([1,1,1,1,1])
    header[1].markdown('<div style="text-align: right;">Valor importado (Mundo): '+"{:.2f}".format(float(st.session_state['peso_importacao_global']))+'</div>',unsafe_allow_html=True)
    header[3].number_input('ImportacaoGlobal',min_value=0.0,max_value=1.0,key='peso_importacao_global',label_visibility='collapsed')


    header = st.columns([1,1,1,1,1])
    header[1].markdown('<div style="text-align: right;">Desvantagem comparativa revelada: '+"{:.2f}".format(float(st.session_state['peso_dcr']))+'</div>',unsafe_allow_html=True)
    header[3].number_input('DCR',min_value=0.0,max_value=1.0,key='peso_dcr',label_visibility='collapsed')


    header = st.columns([1,1,1,1,1])
    header[1].markdown('<div style="text-align: right;">Crescimento: '+"{:.2f}".format(float(st.session_state['peso_crescimento']))+'</div>',unsafe_allow_html=True)
    header[3].number_input('Crescimento',min_value=0.0,max_value=1.0,key='peso_crescimento',label_visibility='collapsed')
    #sliderOportunidades = header[3].slider('Oportunidades.', 0, 100, key='slider_Oportunidades', label_visibility='hidden')

row = st.columns([1,2,5])
peso_pgi=row[0].number_input('PGI',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')
row[1].text('Product Gini index')

row = st.columns([1,2,5])
peso_pei=row[0].number_input('PEI',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')
row[1].text('Product Emission Intensity index')

row = st.columns([1,2,5])
peso_dcr_bloco=row[0].number_input('DCR_bloco',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')
row[1].text('DCR AMS(-Brazil)')

row = st.columns([1,2,5])
peso_proporcao_importacao_brasil_ams=row[0].number_input('Proporcao_importacao_bloco',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')
row[1].text('Proporção importação AMS - Brazil')


row = st.columns([1,7])
peso_ganhos=row[0].number_input('Ganhos',min_value=0.0,max_value=1.0,value=0.3,label_visibility='collapsed')

with row[1].expander("Ganhos de complexidade"):
    header = st.columns([1,1,1,2])
    #header[0].markdown('#### Análise de ganhos')
    header[1].markdown('<div style="text-align: right;">Índice de Complexidade do Produto: '+str(float(st.session_state['slider_Ganhos']/100))+'</div>',unsafe_allow_html=True)
    header[1].markdown('<div style="text-align: right;">Índice de Ganho de Oportunidade: '+str(float((100-st.session_state['slider_Ganhos'])/100))+'</div>',unsafe_allow_html=True)

    sliderGamnhos = header[3].slider('Oportunidades.', 0, 100, key='slider_Ganhos', label_visibility='hidden')


#st.form_submit_button('Atualizar ranking')

###Capacidades Atuais
peso_valor_exportado = st.session_state['slider_CapacidadesAtuais'][0]/100
peso_vcr = (st.session_state['slider_CapacidadesAtuais'][1]-st.session_state['slider_CapacidadesAtuais'][0])/100
peso_densidade_produto = (100-st.session_state['slider_CapacidadesAtuais'][1])/100

#peso_capacidade_atuais = 0.33

#Oportunidades de mercado
peso_valor_importado = st.session_state['peso_importacao']
peso_valor_importado_total = st.session_state['peso_importacao_global']
peso_dcr = st.session_state['peso_dcr']
peso_crescimento = st.session_state['peso_crescimento']

#peso_oportunidaes = 0.33

#Análise de ganhos
peso_complexidade_produto = st.session_state['slider_Ganhos']/100
peso_igo = (100-st.session_state['slider_Ganhos'])/100
#peso_ganhos = 0.5



df['valor_indice'] = peso_capacidade_atuais*(peso_valor_exportado*df['export_value_normalized'] + \
                                                              peso_vcr*df['rca_normalized'] + peso_densidade_produto*df['density_normalized'])+\
    (peso_oportunidaes/(peso_valor_importado+peso_valor_importado_total+peso_dcr+peso_crescimento))*(peso_valor_importado*df['import_value_normalized'] + peso_valor_importado_total*df['import_value_total_normalized']\
                   + peso_dcr*df['rcd_normalized'] +peso_crescimento*df['growth_normalized'] ) + \
     peso_ganhos*(peso_complexidade_produto*df['pci_gt_mean'] + peso_igo*df['cog_normalized'])  + peso_pgi*df['pgi_normalized_inverted']   \
        + peso_pei*df['pei_normalized_inverted'] + peso_dcr_bloco*df['dcr_bloco_normalized'] + peso_proporcao_importacao_brasil_ams*df['proporcao_importacao_origem_brasil']


df_plot = df[['valor_indice','hs_product_code','hs_product_name_short_en','dcr_bloco','proporcao_importacao_origem_brasil','export_value','rca','growth','density','import_value','import_value_total','rcd','pci','cog','pgi','pei']]


df_plot['hs_product_code'] = df_plot['hs_product_code'].apply(str)

df_plot['rca'] = df_plot['rca'].map('{:.2f}'.format)
df_plot['density'] = df_plot['density'].map('{:.2f}'.format)
df_plot['rcd'] = df_plot['rcd'].map('{:.2f}'.format)
df_plot['pci'] = df_plot['pci'].map('{:.2f}'.format)
df_plot['cog'] = df_plot['cog'].map('{:.2f}'.format)
df_plot['pgi'] = df_plot['pgi'].map('{:.2f}'.format)
df_plot['dcr_bloco'] = df_plot['dcr_bloco'].map('{:.2f}'.format)
df_plot['proporcao_importacao_origem_brasil'] = df_plot['proporcao_importacao_origem_brasil'].map('{:.2f}'.format)


df_plot['export_value'] = df_plot['export_value']/1000000
df_plot['export_value'] = df_plot['export_value'].map('${:,.2f}'.format)

df_plot['growth'] = df_plot['growth']/1000000
df_plot['growth'] = df_plot['growth'].map('${:,.2f}'.format)


df_plot['import_value'] = df_plot['import_value']/1000000
df_plot['import_value'] = df_plot['import_value'].map('${:,.2f}'.format)

df_plot['import_value_total'] = df_plot['import_value_total']/1000000
df_plot['import_value_total'] = df_plot['import_value_total'].map('${:,.2f}'.format)

df_plot['pei'] = df_plot['pei']/1000
df_plot['pei'] = df_plot['pei'].map('{:,.2f}'.format)



df_plot['rank'] = df_plot['valor_indice'].rank(method='dense',ascending=False)
df_plot = df_plot[['rank','valor_indice','hs_product_code','hs_product_name_short_en','dcr_bloco','proporcao_importacao_origem_brasil','export_value','rca','density','import_value','import_value_total','growth','rcd','pci','cog','pgi','pei']]

filtro_sh4 = st.text_input('Digite o SH4 desejado:')
df_plot = df_plot[df_plot['hs_product_code'].str.startswith(filtro_sh4)]

df_plot = df_plot.rename(columns={'dcr_bloco' : 'DCR AMS-BR','proporcao_importacao_origem_brasil' : 'Prop. de imp. com orig. Brasil (AMS)','hs_product_code' : ' Código HS 2007','hs_product_name_short_en': 'Descrição', 'export_value' : 'Exp (Milhões)','growth' : 'Crescimento (Milhões 2013-2021)', 'import_value' : 'Imp. (Milhões)','import_value_total' : 'Imp. Mundo (Milhões)', 'rca' : 'VCR', 'density' : 'Dens.', 'rcd' : 'DCR', 'pci' : 'ICP','cog' : 'Ganho de Op.','rank' : 'Rank','pgi' : 'PGI', 'pei' : 'PEI (Mil)'} )


st.dataframe(df_plot.drop('valor_indice',axis=1).sort_values(by='Rank'), use_container_width=True,hide_index =True)
