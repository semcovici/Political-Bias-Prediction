import streamlit as st
import pandas as pd
import variables
from PIL import Image
import joblib
from aux_func import *
import gc

# setting page general config
st.set_page_config(page_title="Classificador de Viés Político", layout="wide", page_icon=Image.open("each.png"))

def main():

    if "bert_model" not in st.session_state.keys():
        st.session_state["bert_model"] = joblib.load('bert_model.pkl')
    bert_model = st.session_state["bert_model"]

    st.sidebar.image('each_2.png')
    st.sidebar.title(f"**Classificador de Viés Político**")
    st.sidebar.subheader('Membros do Projeto:')
    st.sidebar.caption("""
    Yago Primerano Arouca\n
    Pedro Semcovici\n
    Andre Hyun Woo Kim Cho\n
    Guilherme Faria do Nascimento\n
    Thiago Eidi Sumida\n
    Lucas Yudi Pó\n
    Nilton Tadashi Enta\n
    Ryan Alexsander Forti\n
    """)
    artigo = st.text_area(
        label='Insira o texto para gerar a previsão de viés político: ',
        height=375
    )
    cols = st.columns([1, 5, 3])
    with cols[0]:
        response = st.button('Gerar Classificação')
    if response: 
        if artigo == '':
            with cols[1]:
                st.warning('**Insira algum texto para classificar!**')
        else:
            artigo = tratar_artigo(artigo)
            input_model = aplicar_bert_embedding(artigo, bert_model)
            vies, fig = classificar_artigo(input_model)
            with cols[1]:
                st.success(f'O texto acima foi classificada como viés de **{vies}**')
            st.plotly_chart(fig, use_container_width=True)
    gc.collect()
                        
main()
for style in variables.markdown:
    st.markdown(style, unsafe_allow_html=True)


# streamlit run interface.py --theme.primaryColor='#000000' --theme.backgroundColor='#EEEEEE' --theme.secondaryBackgroundColor='#FFE8C0' --theme.textColor='#000000' --theme.font='sans serif'