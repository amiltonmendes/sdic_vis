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


tab1, tab2, tab3, tab4 = st.tabs(["Capacidades atuais", "Oportunidades", "Ganhos de complexidade","Externalidades"])

with tab1:

    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">Capacidades atuais</div>',unsafe_allow_html=True,help="Peso dado ao grupo das variáveis abaixo no cálculo do ranking")
    peso_capacidade_atuais = row[1].number_input('capacidade',min_value=0.2,max_value=0.4,value=0.3,label_visibility='collapsed')
    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Valor exportado</div>',unsafe_allow_html=True, help="Peso do valor das exportações brasileiras do produto")
    peso_valor_exportado = row[1].number_input('Exportação',min_value=0.0,max_value=0.5,value=0.33,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Vantagem comparativa revelada</div>',unsafe_allow_html=True, help="""Peso da vantagem comparativa revelada (VCR).\nValores de VCR acima de 1 indicam que o produto representa mais para a pauta exportadora brasileira do que a média mundial, ou seja, o país é competitivo em relação a esse produto.""")
    peso_vcr = row[1].number_input('vcr',min_value=0.0,max_value=0.5,value=0.33,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Densidade do produto</div>',unsafe_allow_html=True,help="Peso da densidade do produto.\nValores mais altos de densidade indicam uma maior proximidade de determinado produto com a estrutura produtiva atual do país do que outros com valores de densidade mais baixos.")
    peso_densidade_produto = row[1].number_input('densidade',min_value=0.0,max_value=0.8,value=0.33,label_visibility='collapsed')


with tab2:
    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">Oportunidades</div>',unsafe_allow_html=True,help="Peso dado ao grupo das variáveis abaixo no cálculo do ranking.")
    peso_oportunidaes=row[1].number_input('Oportunidades',min_value=0.2,max_value=0.4,value=0.3,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Valor importado</div>',unsafe_allow_html=True,help="Peso das importações brasileiras do produto")
    peso_importacao = row[1].number_input('peso_importacao',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed')


    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Valor importado (Mundo)</div>',unsafe_allow_html=True,help="Peso das importações mundiais do produto")
    peso_importacao_global = row[1].number_input('Importacao Global',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Desvantagem comparativa revelada</div>',unsafe_allow_html=True,help="Peso da desvantagem comparativa revelada (DCR).\nValores de DCR acima de 1 indicam que o produto representa mais para a pauta importadora brasileira do que a média mundial, ou seja, o país é dependente de importações em relação a esse produto.")
    peso_dcr = row[1].number_input('DCR',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Crescimento de importações (2021 - 2013)</div>',unsafe_allow_html=True,help="Peso do crescimento das importações mundiais do produto, calculado a partir da subtração das importações totais do ano de 2021 pelas do ano de 2013.")
    peso_crescimento = row[1].number_input('Crescimento',min_value=0.0,max_value=1.0,value=0.1,label_visibility='collapsed')




with tab3:
    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">Ganhos de complexidade</div>',unsafe_allow_html=True,help="Peso dado ao grupo de variáveis abaixo no cálculo do ranking.")
    peso_ganhos=row[1].number_input('Ganhos',min_value=0.4,max_value=0.8,value=0.5,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Índice de Complexidade do Produto</div>',unsafe_allow_html=True, help="Peso do índice de complexidade do produto (ICP). Mede a diversidade e a sofisticação da expertise necessária para fabricar um produto. O ICP é calculado a partir de quantos outros países podem fabricar o produto, assim como a complexidade econômica desses países.")
    peso_indice_complexidade = row[1].number_input('Índice complexidade',min_value=0.3,max_value=0.8,value=0.5,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Índice de Ganho de Oportunidade</div>',unsafe_allow_html=True,help="Peso do índice de ganho de oportunidade. O índice de ganho de oportunidade mede o quanto um país pode se beneficiar com a diversificação futura a partir do desenvolvimento de um produto em particular. Dessa forma, o valor estratégico de um produto é baseado nas possibilidades de diversificação para setores mais complexos que são abertas.")
    peso_indice_ganho_oportunidade = row[1].number_input('Ganho oportunidade',min_value=0.3,max_value=0.8,value=0.5,label_visibility='collapsed')


        
with tab4:

    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">Externalidades</div>',unsafe_allow_html=True)
    peso_externalidades = row[1].number_input('externalidades',min_value=0.0,max_value=0.2,value=0.1,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Product Gini index</div>',unsafe_allow_html=True)
    peso_pgi = row[1].number_input('peso_pgi',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Product Emission Intensity index</div>',unsafe_allow_html=True)
    peso_pei = row[1].number_input('PEI',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')


    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">Impacto no bloco América do Sul, exceto Brasil</div>',unsafe_allow_html=True)
    peso_impacto_ams = row[1].number_input('Impacto AMS',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')




###Capacidades Atuais


componente_capacidades_atuais = (peso_capacidade_atuais/ (peso_valor_exportado+peso_vcr+peso_densidade_produto))*\
    (peso_valor_exportado*df['export_value_normalized'] + peso_vcr*df['rca_normalized'] + peso_densidade_produto*df['density_normalized'])
    
componente_oportunidades = (peso_oportunidaes/(peso_importacao+peso_importacao_global+peso_dcr+peso_crescimento))*(peso_importacao*df['import_value_normalized'] + peso_importacao_global*df['import_value_total_normalized']\
                   + peso_dcr*df['rcd_normalized'] +peso_crescimento*df['growth_normalized'] ) 

componente_ganhos = (peso_ganhos/(peso_indice_ganho_oportunidade+peso_indice_complexidade))*(peso_ganhos*df['pci_gt_mean'] + peso_indice_ganho_oportunidade*df['cog_normalized'])  

#Criar o indice de impacto AMS
df['impacto_ams'] = 1 - df['proporcao_importacao_origem_brasil']
df.loc[df['dcr_bloco']<=1,'impacto_ams'] = 0

componentes_externalidades = peso_externalidades/(peso_impacto_ams+peso_pei+peso_pgi)*(peso_pei*df['pei_normalized_inverted'] + peso_pgi*df['pgi_normalized_inverted'] + peso_impacto_ams*df['impacto_ams'])


df['valor_indice'] =  componente_capacidades_atuais +  componente_oportunidades + componente_ganhos + componentes_externalidades


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
