import streamlit as st
import pandas as pd

st.title('Умный (не очень) поиск сериалов')
st.divider()
user_input = st.text_input("Чего желаешь посмотреть")
col1, col2 = st.columns([8, 1])  # Правая колонка меньше
with col2:
    click = st.button("Найти")

if click:
    pass