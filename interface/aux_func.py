import pandas as pd 
from sklearn.preprocessing import MaxAbsScaler
from sklearn.model_selection import train_test_split
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import RandomOverSampler
from sklearn.feature_selection import SelectKBest
from xgboost import XGBClassifier
import numpy as np
import joblib
import unicodedata
from transformers import AutoTokenizer  
from transformers import AutoTokenizer  
from transformers import TFBertModel, BertModel
import torch
import plotly.graph_objects as go

def tratar_artigo(artigo):
    artigo = artigo.lower()
    artigo = ''.join(artigo.split('.')[:-2])

    partidos = [
        'novo', 'pcb', 'pdt', 
        'pl', 'pp', 'psol', 'pstu', 
        'mdb', 'pcdob', 'psb', 'pt', 
        'pv', 'rede', 'união brasil'
    ]
    for partido in partidos:
        artigo = artigo.replace(f' {partido} ', ' ')
        
    artigo = ' '.join(word for word in artigo.split(' ') if word.isalnum())
    artigo = unicodedata.normalize('NFKD', artigo)
    artigo = artigo.encode('ASCII', 'ignore')
    artigo = artigo.decode('utf-8')
    artigo = artigo.replace('[^a-zA-Z]', ' ')
    for n in range(30):
        artigo = artigo.replace('  ', ' ')
    return artigo

def bert_text_preparation(text, tokenizer):
    marked_text = "[CLS] " + text + " [SEP]"
    tokenized_text = tokenizer.tokenize(marked_text, truncation=True, max_length=512, padding = True)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = [1]*len(indexed_tokens)
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])
    return tokenized_text, tokens_tensor, segments_tensors

def get_bert_embeddings(tokens_tensor, segments_tensors, model):
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2][1:]
    token_embeddings = hidden_states[-1]
    token_embeddings = torch.squeeze(token_embeddings, dim=0)
    list_token_embeddings = [token_embed.tolist() for token_embed in token_embeddings]
    return list_token_embeddings

def aplicar_bert_embedding(artigo, bert_model):
    tokenizer = joblib.load('tokenizer.pkl')
    tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(artigo, tokenizer)
    list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, bert_model)
    bert_emb = np.array(list_token_embeddings).mean(axis=0)
    input_model = pd.DataFrame(
        data=bert_emb, 
        index=[f"emb_{i + 1}" for i in range(len(bert_emb))]
    ).T
    return input_model

def classificar_artigo(input_model):
    pipeline = joblib.load('pipeline.pkl')
    pred = pipeline.predict(input_model)[0]
    predict_proba = pipeline.predict_proba(input_model)[0]
    if pred == 0:
        pred = 'Esquerda'
    elif pred == 1:
        pred = 'Centro'
    else:
        pred = 'Direita'
    return pred, get_plot(predict_proba.round(4))

def get_plot(predict_proba):
    prob_df = pd.DataFrame({
        'Esquerda': predict_proba[0],
        'Centro': predict_proba[1],
        'Direita': predict_proba[2]
    }, index=[1]).T
    fig = go.Figure(
        go.Bar(
            x=prob_df[1],
            y=prob_df.index,
            orientation='h',
            marker=dict(color = 'orange'),
            marker_line=dict(width=1, color='#6e2f0b')
        )
    )
    fig.update_layout(
        xaxis_title="Probabilidade", 
        yaxis_title="Viés",
        yaxis=dict(tickfont=dict(color="#6e2f0b")),
        xaxis=dict(tickfont=dict(color="#6e2f0b")),
        xaxis_range = [0,1],
        width=800,
        height=375
    )
    fig.update_xaxes(
        showline=True, 
        linewidth=2, 
        linecolor='#6e2f0b', 
        gridcolor='#F67C41', 
        tickcolor='#6e2f0b', 
        tickfont=dict(size=16),
        title=dict(font=dict(size=16)),
        title_font_color="#6e2f0b", 
        color="#6e2f0b"
    )
    fig.update_yaxes(
        showline=True, 
        linewidth=2, 
        linecolor='#6e2f0b', 
        gridcolor='#F67C41', 
        tickcolor='#6e2f0b', 
        tickfont=dict(size=16),
        title=dict(font=dict(size=16)),
        title_font_color="#6e2f0b", 
        color="#6e2f0b"
    )
    return fig