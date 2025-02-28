import streamlit as st
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_resource
def load_data():
    return pd.read_csv('data/to_translate_df.csv', index_col='Unnamed: 0')


@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data
def load_vectors():
    return torch.load("models/description_vectors_MiniLM-L12-v2.pt")


def search_series(query, top_k=5):
    query_vector = model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(query_vector.cpu(), description_vectors.cpu())[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    results = df.iloc[top_indices][["title", "description", "image_url", "genres"]].copy()
    results["similarity (%)"] = (similarities[top_indices] * 100).round(2)
    return results

# UI

st.title('Умный (не самый) поиск сериалов')
st.write('Использовалась модель MiniLM-L12-v2')
st.divider()
user_input = st.text_input("Чего желаешь посмотреть")
col2, col1, col3 = st.columns([2, 5,1])
with col3:
    click = st.button("Найти")
with col2:
    n = st.number_input('Топ', 0, 50, value=10 , step=5)
if click:
    df = load_data()
    model = load_model()
    description_vectors = load_vectors()

    results = search_series(user_input,n)
    for i in range(n):
        st.subheader(results.iloc[i]['title'])
        st.write(f"**Жанры:** {results.iloc[i]['genres']}")
        st.write(f"**Процент схожести:** {round(results.iloc[i]['similarity (%)'])}%")
        st.image(results.iloc[i]['image_url'])
        st.write(results.iloc[i]['description'])
        st.divider()
