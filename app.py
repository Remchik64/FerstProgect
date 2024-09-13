import streamlit as st
import requests
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from tinydb import TinyDB, Query
import page1
from streamlit_extras.switch_page_button import switch_page

API_URL = "https://flowise-renataraev64.amvera.io/api/v1/prediction/35ca3102-682b-46eb-b4dc-cb372b42634d"

# Инициализируем базы данных
chat_db = TinyDB('chat_history.json')
user_db = TinyDB('user_database.json')

@st.cache_data(ttl=3600)  # Кэшируем данные на 1 час
def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

# Инициализируем историю сообщений
history = StreamlitChatMessageHistory(key="chat_messages")

# Пример запроса к API с сессией чата
output = query({
    "question": "Hello",
    "overrideConfig": {
        "sessionId": "chat2"
    }
})

# Используйте session_state для хранения состояния
if "chat_cleared" not in st.session_state:
    st.session_state.chat_cleared = False

# Инициализируем контейнер для вывода ответов
response_container = st.empty()

def display_response(response):
    # Очищаем контейнер и выводим новый ответ
    response_container.empty()
    response_container.write(response)

def clear_chat():
    chat_db.truncate()  # Очищаем базу данных
    history.clear()  # Очищаем историю сообщений
    st.session_state.user_input = ""  # Очищаем поле ввода
    st.session_state.messages = []  # Очищаем сообщения в сессии
    st.success("Чат очищен!")  # Увдомление об успешной очистке
    st.session_state.chat_cleared = True  # Устанавливаем флаг очистки чата

# Кнопка очистки чата
clear_chat_button = st.sidebar.button("Очистить чат", on_click=clear_chat)

# Проверяем, был ли чат очищен, и обновляем страницу только в этом случае
if st.session_state.chat_cleared:
    st.session_state.chat_cleared = False  # Сбрасываем флаг
    st.experimental_rerun()  # Обновляем страницу

# Создаем кнопки в боковой панели
page1_button = st.sidebar.button("Page1")
home_button = st.sidebar.button("Вернуться на стартовую страницу")

# Функция для отображения страниц
def show_page(page_name):
    if page_name == "Page1":
        page1.show_page1()
    elif page_name == "Start":
        st.title("Стартовая страница")
        st.text("Добро пожаловать в мой чат-бот!")
        
        # Загужаем историю сообщений из базы данных
        chat_history = chat_db.all()  # Исправлено на chat_db
        for msg in chat_history:
            st.chat_message(msg["role"]).write(msg["content"])
        
        def submit_question():
            user_input = st.session_state.user_input
            payload = {"question": user_input}
            output = query(payload)
            response_text = output.get('text', '')
            display_response(response_text)
            
            # Сохраняем сообщения в историю
            history.add_user_message(user_input)
            history.add_ai_message(response_text)
            
            # Сохраняем сообщения в базу данных
            chat_db.insert({"role": "user", "content": user_input})  # Исправлено на chat_db
            chat_db.insert({"role": "assistant", "content": response_text})  # Исправлено на chat_db
            
            # Очищаем поле ввода
            st.session_state.user_input = ""

        st.text_input("Введите ваш вопрос", key="user_input", on_change=submit_question)

# Инициализируем session_state
if "page" not in st.session_state:
    st.session_state.page = "Start"
# Проверяем, какой кнопкой был кликнут
if page1_button:
    st.session_state.page = "Page1"
elif home_button:
    st.session_state.page = "Start"
# Отображаем соответствующую страницу
show_page(st.session_state.page)