import streamlit as st
import requests
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from tinydb import TinyDB, Query
import page1

from streamlit_extras.switch_page_button import switch_page

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    switch_page("registr")

st.set_page_config(page_title="Чат-бот", layout="wide")

API_URL = "https://flowise-renataraev64.amvera.io/api/v1/prediction/80c6baef-f33a-4c39-9516-1db9fb658b67"

# Инициализируем базы данных
chat_db = TinyDB('chat_history.json')
user_db = TinyDB('user_database.json')

# Инициализируем атрибуты для подсчета токенов, если они не существуют
if "tokens_used" not in st.session_state:
    st.session_state.tokens_used = 0  # Инициализация с��етчика токенов

# Инициализируем атрибуты для доступных символов, если они не существуют
if "available_symbols" not in st.session_state:
    st.session_state.available_symbols = 0  # Инициализация доступных символов

@st.cache_data(ttl=3600)  # Кэшируем данные на 1 час
def query(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()
    except requests.RequestException as e:
        st.error(f"Ошибка при запросе к API: {e}")  # Обработка ошибок
        return {}

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
    history.clear()  # Очищаем истрию сообщений
    st.session_state.user_input = ""  # Очищаем поле ввода
    st.session_state.messages = []  # Очищаем сообщения в сессии
    st.success("Чат очищен!")  # Увдомление об успешной очистке
    st.session_state.chat_cleared = True  # Устанавливаем флаг очистки чата

# Кнопка очистки чата
clear_chat_button = st.sidebar.button("Очистить чат", on_click=clear_chat)

# роверяем, был ли чат очищен, и обновляем страницу только в этом случае
if st.session_state.chat_cleared:
    st.session_state.chat_cleared = False  # Сбрасываем флаг
    st.rerun()  # Обновляем страницу

# Создаем кнопки в боковой панели
page1_button = st.sidebar.button("Чат 2")
home_button = st.sidebar.button("Старт")
profile_button = st.sidebar.button("Лич��ый кабинет")

# Функция для отображения страниц
def show_page(page_name):
    if page_name == "Page1":
        page1.show_page1()
    elif page_name == "Start":
        if "logged_in" in st.session_state and st.session_state.logged_in:
            st.title(f"Добро пожаловать, {st.session_state.username}!")
        else:
            st.title("Стартовая страница")
        st.text("Добро пожаловать в мой чат-бот!")

        # Отображаем счетик использованных токенов
        st.header("Использованные токены")
        st.write(f"Количество использованных токенов: {st.session_state.tokens_used}")

        # Загружаем историю сообщений из базы данных
        chat_history = chat_db.all()
        for msg in chat_history:
            st.chat_message(msg["role"]).write(msg["content"])
        
        def submit_question():
            user_input = st.session_state.user_input
            if st.session_state.available_symbols <= 0:
                st.warning("У вас закончились символы. Пожалуйста, пополните баланс!")  # Уведомление о недостатке символов
                return  # Прекращаем выполнение, если символы закончились

            payload = {"question": user_input}
            output = query(payload)
            response_text = output.get('text', '')
            display_response(response_text)
            
            # Сохраняем сообщения в историю
            history.add_user_message(user_input)
            history.add_ai_message(response_text)
            
            # Сохраняем сообщения в базу данных
            chat_db.insert({"role": "user", "content": user_input})
            chat_db.insert({"role": "assistant", "content": response_text})
            
            # Увеличиваем счетчик использованных символов на количество символов в ответе
            if response_text:  # Проверяем, что ответ не пустой
                st.session_state.tokens_used += len(response_text)  # Добавляем количество символов в ответе
                st.session_state.available_symbols -= len(response_text)  # Уменьшаем доступные символы

            # Проверяем, достиг ли по��ьзователь лимита символов
            if st.session_state.tokens_used >= 1000:
                st.warning("Вы использовали 1000 символов. Пожалуйста, пополните баланс!")  # Уведомление о необходимости пополнения

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
elif profile_button:
    switch_page("profile")
# Отображаем соответствующую страницу
show_page(st.session_state.page)