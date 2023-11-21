from transformers import AutoTokenizer  # Or BertTokenizer
from transformers import AutoTokenizer  # Or BertTokenizer
from transformers import BertModel
import torch
import tqdm
import pandas as pd
import numpy as np
import datetime


################ Data Path #################################
data_input_path = '../../dataset/processed/artigos_tratados/artigos_tratados.parquet'
data_output_path = "../../dataset/processed/artigos_tratados/bertimbau/artigos_tratados_bert_lg.parquet"
############################################################


################ Aux Functions #############################
"""
ref: https://towardsdatascience.com/3-types-of-contextualized-word-embeddings-from-bert-using-transfer-learning-81fcefe3fe6d
"""
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
############################################################


# import of models 
tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-large-portuguese-cased', do_lower_case=False)
model = BertModel.from_pretrained('neuralmind/bert-large-portuguese-cased', output_hidden_states = True)


# get data
data = pd.read_parquet(data_input_path)
data_bert = data.copy()

emb_list = list()

j = 0
len_df = data_bert.shape[0]
print(f'Start of Embeddding. Datetime: {datetime.datetime.today()}')
for i, row in data_bert.iterrows():

    text = row['Conteudo']
    label = row['Vies']

    
    
    tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(text, tokenizer)
    
    list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model)
    
    bert_emb = np.array(list_token_embeddings).mean(axis=0)
    bert_emb = np.concatenate([row, bert_emb])
    emb_list.append(bert_emb)
    
    if j % 100 == 0:
        print(f'Progress: {j}/{len_df - 1}. Datetime: {datetime.datetime.today()}')
        
    j += 1
        
print(f'End of Embedding. Datetime: {datetime.datetime.today()}')


    
columns = np.concatenate([data_bert.columns, [f"emb_{i + 1}" for i in range(len(emb_list[0]) - data_bert.shape[1])]])

df_bert = pd.DataFrame(emb_list, columns=columns)

df_bert.to_parquet(data_output_path, index = False)