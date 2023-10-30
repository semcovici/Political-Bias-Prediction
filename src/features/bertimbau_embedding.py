from transformers import AutoTokenizer  # Or BertTokenizer
from transformers import AutoTokenizer  # Or BertTokenizer
from transformers import BertModel
import torch
import tqdm
import pandas as pd
import numpy as np
import datetime

import sys

################ Data Path #################################
input_folder_path = '../../dataset/raw/dados_treino_pt_google_trad/'
output_path_folder = "../../dataset/processed/dados_treino_pt_google_trad/bertimbau/"


list_files = []
list_index = []
for i in range(5):
    
    input_forlder_filename = f'parte_{i + 1}.parquet'
    
    file = pd.read_parquet(input_folder_path + input_forlder_filename)
    
    list_files.append(file)
    
data = pd.concat(list_files)
############################################################


################ Aux Functions #############################
"""
ref: https://towardsdatascience.com/3-types-of-contextualized-word-embeddings-from-bert-using-transfer-learning-81fcefe3fe6d
"""
def bert_text_preparation(text, tokenizer):
    marked_text = "[CLS] " + text + " [SEP]"
    tokenized_text = tokenizer.tokenize(marked_text)
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
############################################################

# import of models 
tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)
model = BertModel.from_pretrained('neuralmind/bert-base-portuguese-cased', output_hidden_states = True)

# get data
#data = get_data(data_input_path)
data_bert = data[data.conteudo.str.len() <= 510]
#data_bert = data

emb_list= list()


j = 0
len_df = data_bert.shape[0]
print(f'Start of Embeddding. Datetime: {datetime.datetime.today()}')
for i, row in data_bert.iterrows():

    #username, comment, created_utc = row
    text = row['conteudo']
    title = row['titulo']
    label = row['rotulo_texto']
    
    tokenized_text, tokens_tensor_text, segments_tensors_text = bert_text_preparation(text, tokenizer)
    tokenized_title, tokens_tensor_title, segments_tensors_title = bert_text_preparation(title, tokenizer)
    
    
    bert_emb_text = np.array(get_bert_embeddings(tokens_tensor_text, segments_tensors_text, model)).mean(axis=0)
    bert_emb_title = np.array(get_bert_embeddings(tokens_tensor_title, segments_tensors_title, model)).mean(axis=0)
    bert_emb = np.concatenate([row, bert_emb_text, bert_emb_title])
    emb_list.append(bert_emb)
    
    if j % 100 == 0:
        print(f'Progress: {j}/{len_df - 1}. Datetime: {datetime.datetime.today()}')
        
    j += 1
        
print(f'End of Embedding. Datetime: {datetime.datetime.today()}')


    
columns = np.concatenate([data_bert.columns, [f"emb_title{i}" for i in range(1, 769)], [f"emb_text{i}" for i in range(1, 769)]])

df_bert = pd.DataFrame(emb_list, columns=columns)


for n, ds in enumerate(np.array_split(df_bert, 5)):
    ds.to_parquet(output_path_folder + f'parte_{n+1}.parquet')