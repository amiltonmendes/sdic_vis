##TODO trabalhar com dados de pei per capita ou ligado ao gpd

import pandas as pd
import streamlit as st
import pandas as pd
import locale
from streamlit_extras.switch_page_button import switch_page
from st_aggrid import GridOptionsBuilder, AgGrid


st.set_page_config(layout="wide")

    
def normalize(df,coluna):
    max_ = max(df[coluna])
    min_ = min(df[coluna])
    if min_>0:
        return (df[coluna]-min_)/(max_-min_)
    elif min_<0:
        return (df[coluna]+abs(min_))/(max_-min_)
    else:
        return (df[coluna])/(max_)

@st.cache_data
def load_data(rca,pei_percapita):
    locale._override_localeconv = {'thousands_sep': '.'}
    retorno = pd.read_csv('./raw_data_ice_pt.csv',dtype={'hs_product_code': str})

    #retorno['hs_product_code'] = retorno['hs_product_code'].apply(str)
    #retorno['pei'] = retorno['pei']/1000

    retorno['export_value'] = retorno['export_value']/1000000

    retorno['import_value'] = retorno['import_value']/1000000

    retorno['impacto_ams'] = 1 - retorno['proporcao_importacao_origem_brasil']
    retorno['impacto_ams'] = retorno['dcr_bloco']*retorno['impacto_ams']
    retorno['impacto_ams'] = normalize(retorno,'impacto_ams')

    ##pgi
    retorno = retorno.merge(pd.read_csv('./raw_data_pgi.csv',dtype={'hs_product_code': str}),on='hs_product_code')
    retorno['pgi_normalized_inverted'] = 1-retorno['pgi']

    ##pei
    if pei_percapita==False:
        retorno= retorno.merge(pd.read_csv('./raw_data_pei.csv',dtype={'hs_product_code': str}),on='hs_product_code')
        retorno['pei_normalized_inverted'] = 1-retorno['pei_standarized']
    else:
        retorno = retorno.merge(pd.read_csv('./raw_data_pei_percapita.csv',dtype={'hs_product_code': str}),on='hs_product_code')
        retorno['pei_normalized_inverted'] = 1-retorno['pei_standarized']

    #pei_normalized_inverted'] + peso_pgi*df['pgi_normalized_inverted
    ##Crescimento
    retorno = retorno.merge(pd.read_csv('./raw_data_import_total_2013.csv',dtype={'hs_product_code': str}),on='hs_product_code')
    
    retorno['growth'] = (retorno['import_value_total']-retorno['import_total_2013'])/retorno['import_total_2013']
    retorno['growth'] = retorno['growth']*100

    retorno['import_value_total'] = retorno['import_value_total']/1000000




    if rca==False:
        retorno = retorno[retorno['rca']<1]
    return retorno

considerar_rca = st.checkbox('Considerar valores de RCA acima de 1?')
considerar_pei_percapita = st.checkbox('Considerar emissões per capita no lugar de emissões totais ?')


#bt_redirecionar = st.button('Analisar produtos')


df = load_data(considerar_rca,considerar_pei_percapita)




tab1, tab2, tab3, tab4 = st.tabs(["1. Capacidades atuais", "2. Oportunidades", "3. Ganhos de complexidade","4. Externalidades"])

with tab1:

    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">1. <b>Capacidades atuais</b></div>',unsafe_allow_html=True,help='Peso dado ao grupo das variáveis abaixo no cálculo do ranking')
    peso_capacidade_atuais = row[1].number_input('capacidade',min_value=0.0,max_value=1.0,value=0.3,label_visibility='collapsed',help='teste')
    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">1.1 Valor exportado</div>',unsafe_allow_html=True, help="Peso do valor das exportações brasileiras do produto")
    peso_valor_exportado = row[1].number_input('Exportação',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">1.2 Vantagem comparativa revelada</div>',unsafe_allow_html=True, help="""Peso da vantagem comparativa revelada (VCR).\nValores de VCR acima de 1 indicam que o produto representa mais para a pauta exportadora brasileira do que a média mundial, ou seja, o país é competitivo em relação a esse produto.""")
    peso_vcr = row[1].number_input('vcr',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">1.3 Proximidade do produto</div>',unsafe_allow_html=True,help="Peso da proximidade (densidade) do produto.\nValores mais altos de densidade indicam uma maior proximidade de determinado produto com a estrutura produtiva atual do país do que outros com valores de densidade mais baixos.")
    peso_densidade_produto = row[1].number_input('densidade',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')


with tab2:
    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">2. Oportunidades</div>',unsafe_allow_html=True,help="Peso dado ao grupo das variáveis abaixo no cálculo do ranking.")
    peso_oportunidaes=row[1].number_input('Oportunidades',min_value=0.0,max_value=1.0,value=0.3,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.1 Valor importado</div>',unsafe_allow_html=True,help="Peso das importações brasileiras do produto")
    peso_importacao = row[1].number_input('peso_importacao',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed')


    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.2 Valor importado (Mundo)</div>',unsafe_allow_html=True,help="Peso das importações mundiais do produto")
    peso_importacao_global = row[1].number_input('Importacao Global',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.3 Desvantagem comparativa revelada</div>',unsafe_allow_html=True,help="Peso da desvantagem comparativa revelada (DCR).\nValores de DCR acima de 1 indicam que o produto representa mais para a pauta importadora brasileira do que a média mundial, ou seja, o país é dependente de importações em relação a esse produto.")
    peso_dcr = row[1].number_input('DCR',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.4 Crescimento de importações (2013-2021)</div>',unsafe_allow_html=True,help="Peso do crescimento das importações mundiais do produto, calculado a partir da subtração das importações totais do ano de 2021 pelas do ano de 2013.")
    peso_crescimento = row[1].number_input('Crescimento',min_value=0.0,max_value=1.0,value=0.1,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.5 Oportunidades de integração com América do Sul</div>',unsafe_allow_html=True,help="Oportunidades de integração com América do Sul. Esse índice é calculado da seguinte forma: 1) para valores de DCR da América do Sul, exceto o Brasil, menores que 1, ele recebe o valor 0; 2) caso contrário, recebe o percentual das importações cujas origens não sejam o Brasil, ou seja, que poderiam ser supridas pelo Brasil.")
    peso_impacto_ams = row[1].number_input('Impacto AMS',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')



with tab3:
    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">3. Ganhos de complexidade</div>',unsafe_allow_html=True,help="Peso dado ao grupo de variáveis abaixo no cálculo do ranking.")
    peso_ganhos=row[1].number_input('Ganhos',min_value=0.0,max_value=1.0,value=0.5,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">3.1 Índice de Complexidade do Produto</div>',unsafe_allow_html=True, help="Peso do índice de complexidade do produto (ICP). Mede a diversidade e a sofisticação da expertise necessária para fabricar um produto. O ICP é calculado a partir de quantos outros países podem fabricar o produto, assim como a complexidade econômica desses países.")
    peso_indice_complexidade = row[1].number_input('Índice complexidade',min_value=0.0,max_value=1.0,value=0.5,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">3.2 Índice de Ganho de Oportunidade</div>',unsafe_allow_html=True,help="Peso do índice de ganho de oportunidade. O índice de ganho de oportunidade mede o quanto um país pode se beneficiar com a diversificação futura a partir do desenvolvimento de um produto em particular. Dessa forma, o valor estratégico de um produto é baseado nas possibilidades de diversificação para setores mais complexos que são abertas.")
    peso_indice_ganho_oportunidade = row[1].number_input('Ganho oportunidade',min_value=0.0,max_value=1.0,value=0.5,label_visibility='collapsed')


        
with tab4:

    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">4. Externalidades</div>',unsafe_allow_html=True,help="Peso dado ao grupo de variáveis abaixo no cálculo do ranking.")
    peso_externalidades = row[1].number_input('externalidades',min_value=0.0,max_value=1.0,value=0.1,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">4.1 Product Gini index</div>',unsafe_allow_html=True,help="Peso de 1 - o Índice de gini do produto ( PGI ). O PGI é calculado a partir da média do índice de gini dos países exportadores de determinado produto, ponderada pela importância desse produto na pauta exportadora daqueles países. O índice de gini mede o quão desigual é a distribuição de renda de um país, ou seja, quanto maior, mais desigualdade de renda um país possui. Quanto mais peso for atribuído a esse índice, mais o ranking beneficiará produtos que estão associados a uma menor desigualdade de renda.")
    peso_pgi = row[1].number_input('peso_pgi',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">4.2 Product Emission Intensity index</div>',unsafe_allow_html=True,help="Peso de 1 - o Índice de emissão de produto ( PEI ). O PEI é calculado a partir da média de emissões gases de efeito estufa dos países exportadores de determinado produto, ponderada pela importância desse produto na pauta exportadora daqueles países. Quanto mais peso for atribuído a esse índice, mais o ranking beneficiará produtos que estão associados a uma menor emissão de gases de efeito estufa.")
    peso_pei = row[1].number_input('PEI',min_value=0.0,max_value=1.0,value=0.33,label_visibility='collapsed')





componente_capacidades_atuais = (peso_capacidade_atuais/ (peso_valor_exportado+peso_vcr+peso_densidade_produto))*\
    (peso_valor_exportado*df['export_value_normalized'] + peso_vcr*df['rca_normalized'] + peso_densidade_produto*df['density_normalized'])
    
componente_oportunidades = (peso_oportunidaes/(peso_importacao+peso_importacao_global+peso_dcr+peso_crescimento+peso_impacto_ams))*(peso_importacao*df['import_value_normalized'] + peso_importacao_global*df['import_value_total_normalized']\
                   + peso_dcr*df['rcd_normalized'] +peso_crescimento*df['growth'] + peso_impacto_ams*df['impacto_ams'] ) 

componente_ganhos = (peso_ganhos/(peso_indice_ganho_oportunidade+peso_indice_complexidade))*(peso_ganhos*df['pci_gt_mean'] + peso_indice_ganho_oportunidade*df['cog_normalized'])  


componentes_externalidades = peso_externalidades/(peso_pei+peso_pgi)*(peso_pei*df['pei_normalized_inverted'] + peso_pgi*df['pgi_normalized_inverted'] )


df['valor_indice'] =  componente_capacidades_atuais +  componente_oportunidades + componente_ganhos + componentes_externalidades


df_plot = df[['valor_indice','hs_product_code','hs_product_name_short_en','no_sh4','dcr_bloco','proporcao_importacao_origem_brasil','export_value','rca','growth','density','import_value','import_value_total','rcd','pci','cog','pgi','pei']]



df_plot['rank'] = df_plot['valor_indice'].rank(method='dense',ascending=False)
df_plot = df_plot[['rank','valor_indice','hs_product_code','no_sh4','dcr_bloco','proporcao_importacao_origem_brasil','export_value','rca','density','import_value','import_value_total','growth','rcd','pci','cog','pgi','pei']]


#if bt_redirecionar:
#    st.session_state['df_plot'] = df_plot[['Rank',' Código HS 2007', 'Descrição']]
#    switch_page("Análise de produtos")




gb = GridOptionsBuilder.from_dataframe(df_plot.drop('valor_indice',axis=1).sort_values(by='rank'))
gb.configure_column("pei",header_name=("PEI (Mil)"), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("dcr_bloco",header_name=("DCR AMS-BR"), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("proporcao_importacao_origem_brasil",header_name=('Prop. de imp. com orig. Brasil (AMS)'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("hs_product_code",header_name=('Código HS 2007'), type=["text"])
gb.configure_column("no_sh4",header_name=('Descrição'), type=["text"])
gb.configure_column("export_value",header_name=('Exp (Milhões)'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("growth",header_name=('Crescimento (Milhões 2013-2021)'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("import_value",header_name=('Imp. (Milhões)'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("import_value_total",header_name=('Imp. Mundo (Milhões)'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("rca",header_name=('VCR'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("density",header_name=('Proximidade'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("rcd",header_name=('DCR'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("pci",header_name=('ICP'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("cog",header_name=('Ganho de Op.'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)
gb.configure_column("rank",header_name=('Posição'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=0)
gb.configure_column("pgi",header_name=('PGI'), type=["numericColumn", "numberColumnFilter","customNumericFormat"],precision=2)

gridOptions = gb.build()

AgGrid(
    df_plot.drop('valor_indice',axis=1).sort_values(by='rank'),
    gridOptions=gridOptions,
    height=230,reload_data=True
)