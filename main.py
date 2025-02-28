import streamlit as st
from PIL import Image

st.title("Умный поиск сериалов")

logo = Image.open('images/logo_0.jpeg')
st.image(logo, width=800)

st.write("### Оглавление")
st.write("Для улучшения поиска на стриминговом сервисе мы создали систему семантического поиска, которая учитывает описание сериалов.")

st.write("### Команда проекта:")
st.write("[Илья](https://github.com/lefuuu)")
st.write("[Алина](https://github.com/RenaTheDv)")
st.write("[Даша](https://github.com/DashonokOk)")
