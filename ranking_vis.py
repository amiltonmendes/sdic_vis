"""
# My first app
Here's our first attempt at using data to create a table:
"""

import pandas as pd
import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('./raw_data_ranking_ice_2020.csv')

df = load_data()


##TODO resolver

#with st.form("Configurações"):
st.markdown('### Peso das Capacidades Atuais ( 0,3 )')
header = st.columns([1,1,1])
header[0].markdown('#### Valor exportado')
header[1].markdown('#### Vantagens comparativas relativas')
header[2].markdown('#### Densidade do produto')

rowCapacidadesAtuais = st.columns([1,1,1])
pesoExportacao = rowCapacidadesAtuais[0].slider('Exp.', 0, 100, 33, label_visibility='hidden')
pesoVcr = rowCapacidadesAtuais[1].slider('Vcr.', 0, 100, 33, label_visibility='hidden')
pesoDensidade = rowCapacidadesAtuais[2].slider('Dens.', 0, 100, 33, label_visibility='hidden')



st.markdown('### Oportunidades de mercado ( 0,3 )')
header = st.columns([1,1,1])
header[0].markdown('#### Valor importado')
header[1].markdown('#### Valor importado (Mundo)')
header[2].markdown('#### Desvantagem comparativa relativa')

rowOportunidades = st.columns([1,1,1])
pesoImportacao = rowOportunidades[0].slider('Imp.', 0, 100, 33, label_visibility='hidden')
pesoimpTotal = rowOportunidades[1].slider('ImpTotal.', 0, 100, 33, label_visibility='hidden')
pesoDcr = rowOportunidades[2].slider('Dcr.', 0, 100, 33, label_visibility='hidden')

st.markdown('### Análise de ganhos ( 0,5 )')
header = st.columns([1,1])
header[0].markdown('#### Índice de Complexidade do Produto')
header[1].markdown('#### Índice de Ganho de Oportunidade')

rowGanhos = st.columns([1,1])
pesoComplexidade = rowGanhos[0].slider('Comp.', 0, 100, 50, label_visibility='hidden')
pesoGo = rowGanhos[1].slider('Go.', 0, 100, 50, label_visibility='hidden')

#st.form_submit_button('Atualizar ranking')

###Capacidades Atuais
peso_valor_exportado = pesoExportacao/100
peso_vcr = pesoVcr/100
peso_densidade_produto = pesoDensidade/100

peso_capacidade_atuais = 0.33

#Oportunidades de mercado
peso_valor_importado = pesoImportacao/100
peso_valor_importado_total = pesoimpTotal/100
peso_dcr = pesoDcr/100

peso_oportunidaes = 0.33

#Análise de ganhos
peso_complexidade_produto = pesoComplexidade/100
peso_igo = pesoGo/100
peso_ganhos = 0.5



df['valor_indice'] = peso_capacidade_atuais*(peso_valor_exportado*df['export_value_standarized'] + \
                                                              peso_vcr*df['rca_standarized'] + peso_densidade_produto*df['density_standarized'])+\
    peso_oportunidaes*(peso_valor_importado*df['import_value_standarized'] + peso_valor_importado_total*df['import_value_total_standarized']\
                   + peso_dcr*df['rcd_standarized']) + \
     peso_ganhos*(peso_complexidade_produto*df['pci_standarized'] + peso_igo*df['cog_standarized'])              


df_plot = df[['hs_product_code','hs_product_name_short_en','export_value','rca','density','import_value','import_value_total','rcd','pci','cog','valor_indice']]




df_plot['export_value'] = df_plot['export_value']/1000000
df_plot['export_value'] = df_plot['export_value'].map('${:,.2f}'.format)

df_plot['import_value'] = df_plot['import_value']/1000000
df_plot['import_value'] = df_plot['import_value'].map('${:,.2f}'.format)

df_plot['import_value_total'] = df_plot['import_value_total']/1000000
df_plot['import_value_total'] = df_plot['import_value_total'].map('${:,.2f}'.format)




df_plot['rank'] = df_plot['valor_indice'].rank(method='dense',ascending=False)


df_plot = df_plot.rename(columns={'hs_product_code' : ' Código HS 2007','hs_product_name_short_en': 'Descrição', 'export_value' : 'Exp (Milhões)', 'import_value' : 'Imp. (Milhões)','import_value_total' : 'Imp. Mundo (Milhões)', 'rca' : 'VCR', 'density' : 'Dens.', 'rcd' : 'DCR', 'pci' : 'ICP','cog' : 'Ganho de Op.','rank' : 'Rank'} )
st.dataframe(df_plot.drop('valor_indice',axis=1).sort_values(by='Rank'), use_container_width=True,hide_index =True)
