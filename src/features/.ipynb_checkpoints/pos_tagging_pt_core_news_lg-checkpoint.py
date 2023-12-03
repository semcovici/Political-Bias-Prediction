# install the tagger with "python -m spacy download pt_core_news_lg"

import sys

import numpy as np
#from tensorflow import keras
import spacy
from spacy.lang.pt.examples import sentences 
import pandas as pd


################ Data Path #################################
input_folder_path = '../../dataset/raw/dados_treino_pt_google_trad/'
output_path_folder = "../../dataset/processed/dados_treino_pt_google_trad/authors_pos_pt_core_news_lg/"
txt_column = "conteudo"
############################################################

list_files = []
list_index = []
for i in range(5):
    
    input_forlder_filename = f'parte_{i + 1}.parquet'
    
    file = pd.read_parquet(input_folder_path + input_forlder_filename)
    
    list_files.append(file)
    
data = pd.concat(list_files)


pos_converter = spacy.load("pt_core_news_lg")
pos_texts = [pos_converter(text) for text in data[txt_column]]

pos = np.empty(len(pos_texts), dtype='object')

pos = np.empty(len(pos_texts), dtype='object')
for i in range(len(pos_texts)):
    pos[i] = " ".join([token.pos_ for token in pos_texts[i]])
    
    
data["pos"] = pos


for n, ds in enumerate(np.array_split(data, 5)):
    ds.to_parquet(output_path_folder + f'parte_{n+1}.parquet')