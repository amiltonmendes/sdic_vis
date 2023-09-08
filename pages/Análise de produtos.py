"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st


st.set_page_config(layout="wide")

if 'df_plot' not in st.session_state:
    st.write('Preencha os parâmetros desejados no ranking de parâmetros antes de acessar a página de análise')      
    st.stop()
else:
    st.write('Em construção')      