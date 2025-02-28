import streamlit as st
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch
import pandas as pd

df = pd.read_csv('data/cleaned_df.csv')

labse_model = SentenceTransformer('sentence-transformers/LaBSE')
distilbert_tokenizer = AutoTokenizer.from_pretrained('distilbert-base-multilingual-cased')
distilbert_model = AutoModel.from_pretrained('distilbert-base-multilingual-cased')
tiny2_tokenizer = AutoTokenizer.from_pretrained('cointegrated/rubert-tiny2')
tiny2_model = AutoModel.from_pretrained('cointegrated/rubert-tiny2')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
distilbert_model.to(device)
tiny2_model.to(device)

with open('models/dashas/labse_index.pkl', 'rb') as f:
    labse_index = pickle.load(f)
with open('models/dashas/distilbert_index.pkl', 'rb') as f:
    distilbert_index = pickle.load(f)
with open('models/dashas/tiny2_index.pkl', 'rb') as f:
    tiny2_index = pickle.load(f)

def search_series(query, model, tokenizer=None, index=None, top_k=5):
    if tokenizer:
        inputs = tokenizer([query], return_tensors="pt", padding=True, truncation=True, max_length=128)
        inputs = {key: val.to(device) for key, val in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
        query_embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    else:
        query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    results = df.iloc[indices[0]]
    return results

st.title("Умный поиск сериалов")
st.image("images/logo_1.jpeg", width=800)  # Add your logo here

query = st.text_input("Введите запрос:")
model_choice = st.selectbox("Выберите модель:", ["LaBSE", "DistilBERT", "tiny2"])
top_k = st.slider("Количество результатов:", min_value=1, max_value=20, value=5)

if st.button("Найти"):
    if query:
        if model_choice == "LaBSE":
            results = search_series(query, labse_model, index=labse_index, top_k=top_k)
        elif model_choice == "DistilBERT":
            results = search_series(query, distilbert_model, distilbert_tokenizer, distilbert_index, top_k=top_k)
        elif model_choice == "tiny2":
            results = search_series(query, tiny2_model, tiny2_tokenizer, tiny2_index, top_k=top_k)

        st.write("Результаты поиска:")
        for i, row in results.iterrows():
            st.write(f"**{row['title']}**")
            st.write(row['description'])
            st.image(row['image_url'], width=600)
    else:
        st.write("Пожалуйста, введите запрос.")
