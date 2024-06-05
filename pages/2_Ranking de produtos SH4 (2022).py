import pandas as pd
import streamlit as st
import pandas as pd
import locale
import io

import numpy as np
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
def normalize_log(df,coluna):
    max_ = max(df[coluna])
    min_ = min(df[coluna])
    if min_>0:
        return np.log(df[coluna]-min_)
    elif min_<0:
        return np.log(df[coluna]+abs(min_))
    else:
        return np.log(df[coluna])


@st.cache_data
def load_data(rca,pei_percapita,considerar_pci_eci):
    locale._override_localeconv = {'thousands_sep': '.'}
    retorno = pd.read_csv('./raw_final_sh4_prod_rev22.csv',dtype={'hs_product_code': str})


    #retorno['hs_product_code'] = retorno['hs_product_code'].apply(str)
    #retorno['pei'] = retorno['pei']/1000

    retorno['export_value'] = retorno['export_value']/1000000

    retorno['import_value'] = retorno['import_value']/1000000

    retorno['impacto_ams'] = 1 - retorno['proporcao_importacao_origem_brasil']
    retorno['impacto_ams'] = retorno['dcr_bloco']*retorno['impacto_ams']
    retorno['impacto_ams'] = normalize(retorno,'impacto_ams')

    ##pgi

    retorno = retorno.merge(pd.read_csv('./raw_data_pgish4_rev22.csv',dtype={'hs_product_code': str}),on='hs_product_code')
    retorno['pgi_normalized_inverted'] = -retorno['pgi_standirized_less_one']

    ##pei
    retorno = retorno.merge(pd.read_csv('./raw_data_pei_percapita_sh4_rev22.csv',dtype={'hs_product_code': str}),on='hs_product_code')
    retorno['pei_normalized_inverted'] = (1-retorno['pei_standarized'])
    


    if considerar_pci_eci:
        retorno = retorno[retorno['pci'] > retorno['eci']]

    #pei_normalized_inverted'] + peso_pgi*df['pgi_normalized_inverted
    ##Crescimento
    #retorno = retorno.merge(pd.read_csv('./raw_data_import_total_2013.csv',dtype={'hs_product_code': str}),on='hs_product_code')
    ##retorno['growth'] = (retorno['import_value_total']-retorno['import_value_total_2013'])/retorno['import_value_total_2013']
    ##retorno['growth'] = retorno['growth']*100
    ##retorno['growth_normalized'] = normalize(retorno,'growth')
    retorno['import_value_total'] = retorno['import_value_total']/1000000




    if rca==False:
        retorno = retorno[retorno['rca']<1]
    return retorno

@st.cache_data
def paginar_df(input_df,linhas):
    df = input_df.copy().drop_duplicates()
    df = df.rename(columns={'rank' : 'Posição', 'hs_product_code' : 'HS4', 'no_sh4' : 'Descrição SH4','impacto_ams' : 'Integração AMS','rca' : 'VCR', 'distancia':'Distância','import_value' : 'Importações brasileiras em Mi',
                            'import_value_total' : 'Importações Mundo em Mi','dcr' : 'DCR', 'pci' : 'Complexidade do produto',
                            'cog' : 'Ganho de oportunidade', 'pgi' : 'PGI','pei':'PEI','export_value' : 'Exportações Brasileiras','valor_indice' : 'Índice'})
    try:
        df_ret = [df.loc[i : i - 1 + linhas, :] for i in range(0, len(df), linhas)]
        return df_ret
    except IndexError:
        return df 
    


considerar_rca = st.checkbox('Considerar valores de RCA acima de 1?')
considerar_pei_percapita = True #= st.checkbox('Considerar emissões per capita no lugar de emissões totais ?')

considerar_pci_eci = st.checkbox('Considerar valores de PCI acima do índice brasileiro ?')



#bt_redirecionar = st.button('Analisar produtos')
bt_redirecionar=False

df = load_data(considerar_rca,considerar_pei_percapita,considerar_pci_eci)




tab1, tab2, tab3, tab4 = st.tabs(["1. Capacidades atuais", "2. Oportunidades", "3. Ganhos de complexidade","4. Externalidades"])

with tab1:

    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">1. <b>Capacidades atuais</b></div>',unsafe_allow_html=True,help='Peso dado ao grupo das variáveis abaixo no cálculo do ranking')
    peso_capacidade_atuais = row[1].number_input('capacidade',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed',help='teste')
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
    peso_oportunidaes=row[1].number_input('Oportunidades',min_value=0.0,max_value=1.0,value=0.25,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.1 Valor importado</div>',unsafe_allow_html=True,help="Peso das importações brasileiras do produto")
    peso_importacao = row[1].number_input('peso_importacao',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')


    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.2 Valor importado (Mundo)</div>',unsafe_allow_html=True,help="Peso das importações mundiais do produto")
    peso_importacao_global = row[1].number_input('Importacao Global',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.3 Desvantagem comparativa revelada</div>',unsafe_allow_html=True,help="Peso da desvantagem comparativa revelada (DCR).\nValores de DCR acima de 1 indicam que o produto representa mais para a pauta importadora brasileira do que a média mundial, ou seja, o país é dependente de importações em relação a esse produto.")
    peso_dcr = row[1].number_input('DCR',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')

    #row = st.columns([2,1,4])
    #row[0].markdown('##### <div style="text-align: right;">2.4 Crescimento de importações globais(2013-2021)</div>',unsafe_allow_html=True,help="Peso do crescimento das importações globais do produto, calculado a partir da subtração das importações totais do ano de 2021 pelas do ano de 2013.")
    #peso_crescimento = row[1].number_input('Crescimento',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">2.5 Oportunidades de integração com América do Sul</div>',unsafe_allow_html=True,help="Oportunidades de integração com América do Sul. Esse índice é calculado a partir da multiplicação do percentual das importações cujas origens não sejam o Brasil, ou seja, que poderiam ser supridas pelo Brasil, pela desvantagem comparativa relevada do produto, calculado considerando-se o bloco América do Sul, exceto o Brasil, como um país ")
    peso_impacto_ams = row[1].number_input('Impacto AMS',min_value=0.0,max_value=1.0,value=0.2,label_visibility='collapsed')



with tab3:
    row = st.columns([2,1,4])
    row[0].markdown('#### <div style="text-align: right;">3. Ganhos de complexidade</div>',unsafe_allow_html=True,help="Peso dado ao grupo de variáveis abaixo no cálculo do ranking.")
    peso_ganhos=row[1].number_input('Ganhos',min_value=0.0,max_value=1.0,value=0.4,label_visibility='collapsed')

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
    peso_pgi = row[1].number_input('peso_pgi',min_value=0.0,max_value=1.0,value=0.5,label_visibility='collapsed')

    row = st.columns([2,1,4])
    row[0].markdown('##### <div style="text-align: right;">4.2 Product Emission Intensity index</div>',unsafe_allow_html=True,help="Peso de 1 - o Índice de emissão de produto ( PEI ). O PEI é calculado a partir da média de emissões gases de efeito estufa dos países exportadores de determinado produto, ponderada pela importância desse produto na pauta exportadora daqueles países. Quanto mais peso for atribuído a esse índice, mais o ranking beneficiará produtos que estão associados a uma menor emissão de gases de efeito estufa.")
    peso_pei = row[1].number_input('PEI',min_value=0.0,max_value=1.0,value=0.5,label_visibility='collapsed')


componente_capacidades_atuais = (peso_capacidade_atuais/ (peso_valor_exportado+peso_vcr+peso_densidade_produto))*\
    (peso_valor_exportado*df['export_value_normalized'] + peso_vcr*df['rca_normalized'] + peso_densidade_produto*df['density_normalized'])
    
componente_oportunidades = (peso_oportunidaes/(peso_importacao+peso_importacao_global+peso_dcr+peso_impacto_ams))*(peso_importacao*df['import_value_normalized'] + peso_importacao_global*df['import_value_total_normalized']\
                   + peso_dcr*df['rcd_normalized'] + peso_impacto_ams*df['impacto_ams'] ) 

#componente_ganhos = (peso_ganhos/(peso_indice_ganho_oportunidade+peso_indice_complexidade))*(peso_ganhos*df['pci_gt_mean'] + peso_indice_ganho_oportunidade*df['cog_normalized'])  
componente_ganhos = (peso_ganhos/(peso_indice_ganho_oportunidade+peso_indice_complexidade))*(peso_ganhos*df['pci_normalized'] + peso_indice_ganho_oportunidade*df['cog_normalized'])  


componentes_externalidades = (peso_externalidades/(peso_pei+peso_pgi))*(peso_pei*df['pei_normalized_inverted'] + peso_pgi*df['pgi_normalized_inverted'] )



df['valor_indice'] =  componente_capacidades_atuais +  componente_oportunidades + componente_ganhos + componentes_externalidades


#df_plot = df[['valor_indice','hs_product_code','no_sh4','dcr_bloco','proporcao_importacao_origem_brasil','export_value','rca','growth','density','import_value','import_value_total','rcd','pci','cog','pgi','pei']]
df_plot = df[['valor_indice','hs_product_code','no_sh4','impacto_ams' ,'export_value','rca','distancia','import_value','import_value_total','dcr','pci','cog','pgi','pei']]


df_plot = df_plot.drop_duplicates()
df_plot['rank'] = df_plot['valor_indice'].rank(method='dense',ascending=False)
#df_plot = df_plot.drop('valor_indice',axis=1)
#df_plot = df_plot[['rank','hs_product_code','no_sh4','dcr_bloco','proporcao_importacao_origem_brasil','export_value','rca','density','import_value','import_value_total','growth','rcd','pci','cog','pgi','pei','valor_indice']]
df_plot = df_plot[['rank','hs_product_code','no_sh4','impacto_ams','export_value','rca','distancia','import_value','import_value_total','dcr','pci','cog','pgi','pei','valor_indice']]


if bt_redirecionar:
    st.session_state['df_plot'] = df_plot[['rank','hs_product_code', 'no_sh4']]
    switch_page("Análise de produtos")


busca = st.text_input(label="Digite o código SH4 ou a descrição da posição NCM que você deseja")
if busca != "":
    df_plot = df_plot[(df_plot.hs_product_code.str.contains(busca)) | (df_plot.no_sh4.str.contains(busca))]


top_menu = st.columns(4)
with top_menu[0]:
    sort = st.radio("Ordenar dados", options=["Sim", "Não"], horizontal=1, index=1)
if sort == "Sim":
    with top_menu[1]:
        sort_field = st.selectbox("Ordenar por", options=['Posição no índice','Importações','Complexidade','SH4'])
    with top_menu[2]:
        sort_direction = st.radio(
            "Ordem", options=["⬆️", "⬇️"], horizontal=True
        )
    coluna = ""
    if sort_field == 'Posição no índice':
        coluna='rank'       
    elif sort_field=="Importações":
        coluna='import_value'
    elif sort_field=='Complexidade':
        coluna='pci'
    elif sort_field=='SH4':
        coluna='hs_product_code'

    df_plot = df_plot.sort_values(by=[coluna], ascending=sort_direction == "⬆️",ignore_index=True)
with top_menu[3]:
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_plot\
        .rename(columns={'rank' : 'Posição', 'hs_product_code' : 'HS4', 'no_sh4' : 'Descrição SH4',
                         'impacto_ams' : 'Integração AMS','rca' : 'VCR', 'distancia':'Distância','import_value' : 'Importações brasileiras em Mi',
                            'import_value_total' : 'Importações Mundo em Mi','dcr' : 'DCR', 'pci' : 'Complexidade do produto',
                            'cog' : 'Ganho de oportunidade', 'pgi' : 'PGI','pei':'PEI','export_value' : 'Exportações Brasileiras','valor_indice' : 'Índice'})\
                                .to_excel(writer, sheet_name='Planilha Complexidade', index=False)
        writer.close()
        download2 = st.download_button(
            label="Download arquivo Excel",
            data=buffer,
            file_name='complexidade_sdic.xlsx',
            mime='application/ms-excel'
        )


pagination = st.container()

bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Tamanho da página", options=[25, 50, 100])
with bottom_menu[1]:
    total_pages = (
        int(len(df_plot) / batch_size) if int(len(df_plot) / batch_size) > 0 else 1
    )
    current_page = st.number_input(
        "Página", min_value=1, max_value=total_pages, step=1
    )
with bottom_menu[0]:
    st.markdown(f"Página **{current_page}** de **{total_pages}** ")



pages = paginar_df(df_plot, batch_size)
try:
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)
except IndexError:
    pagination.dataframe(data=pages, use_container_width=True)



