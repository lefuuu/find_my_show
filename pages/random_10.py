import streamlit as st
import pandas as pd
# task 1 sample 10 streamlit



df=pd.read_csv('data/full_df_without_nans.csv')
n=10
rand = df.sample(n, ignore_index=True)
st.title('Cлучайные 10 сериалов ')
st.divider()
st.write('По нажатию на кнопку генерирует случайные 10 сериалов из датасета')
st.divider()
if st.button('Сгенерировать 10 сериалов'):
    for i in range(0,n):
        st.subheader(f"{rand['title'][i]}")
        st.write(f"{rand['description'][i]}")