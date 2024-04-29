import streamlit as st


from sqlalchemy import create_engine

st.set_page_config(
    page_title="Página de avaliação de estratégias para construção do ICE SDIC",
    page_icon="👋",
)

st.sidebar.success("Selecione em uma das estratégias.")

st.markdown(
    """
    Página experimental SDIC.
    
    Selecione uma das estratégias no menu à esquerda.   
"""
)