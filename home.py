import streamlit as st
from streamlit_extras.switch_page_button import switch_page  # Используем функцию переключения страниц

# Установка конфигурации страницы с начальным состоянием боковой панели как "collapsed"
st.set_page_config(page_title="Название вашего приложения", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# Заголовок
st.title("Добро пожаловать в наше приложение")
st.markdown("<h2 style='color: #4B4B4B;'>Эффективное решение для ваших задач</h2>", unsafe_allow_html=True)

# Описание приложения
st.subheader("Что такое наше приложение?")
st.write("Наше приложение разработано для повышения вашей продуктивности и упрощения повседневных задач. Оно использует современные технологии и интуитивно понятный интерфейс.")

# Изображение
st.image("start.jpg", caption="Скриншот нашего приложения", use_column_width=True)

# Функции
st.subheader("Ключевые функции")
col1, col2, col3 = st.columns(3)
with col1:
    st.write("### Функция 1")
    st.write("Описание функции 1")
with col2:
    st.write("### Функция 2")
    st.write("Описание функции 2")
with col3:
    st.write("### Функция 3")
    st.write("Описание функции 3")

# Отзывы пользователей
st.subheader("Отзывы пользователей")
st.write("Наши пользователи любят наше приложение. Вот что они говорят:")
st.write("### Пользователь 1")
st.write("Это приложение изменило мою жизнь. Оно простое в использовании и значительно повысило мою продуктивность.")
st.write("### Пользователь 2")
st.write("Я был скептически настроен, но это приложение превзошло все мои ожидания. Команда поддержки также очень отзывчивая.")

# Кнопка для регистрации
st.markdown("<div class='center-button'>", unsafe_allow_html=True)  # Центрирование кнопки
if st.button("Зарегистрироваться", key="register_button"):  # Изменено на кнопку регистрации
    switch_page("registr")  # Перенаправление на страницу регистрации
st.markdown("</div>", unsafe_allow_html=True)  # Закрытие блока центрирования

# Дополнительная информация
st.subheader("Узнайте больше")
st.write("Если вы хотите узнать больше о нашем приложении, пожалуйста, посетите нашу [страницу FAQ](https://your-website.com/faq).")

# Футер
st.markdown("""
<footer style='text-align: center; color: grey; padding: 10px;'>
    <p style='margin: 0;'>Copyright 2023 Ваша Компания. Все права защищены.</p>
</footer>
""", unsafe_allow_html=True)

# Добавление стилей
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
    }
    h2 {
        color: #2C3E50;
    }
    .stButton {
        background-color: #2980B9;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton:hover {
        background-color: #3498DB;
    }
</style>
""", unsafe_allow_html=True)
