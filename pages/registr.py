import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import requests
from tinydb import TinyDB, Query
import bcrypt  # Импортируем библиотеку для хеширования паролей

st.set_page_config(page_title="Вход/Регистрация", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# Инициализация базы данных пользователей
user_db = TinyDB('user_database.json')

# Функция для регистрации пользователя
def register_user(username, email, password):
    User = Query()
    if user_db.search(User.username == username):
        return False, "Пользователь с таким именем уже существует"
    if user_db.search(User.email == email):
        return False, "Пользователь с таким email уже существует"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Хешируем пароль
    user_db.insert({'username': username, 'email': email, 'password': hashed_password.decode('utf-8')})  # Сохраняем хешированный пароль
    return True, "Регистрация успешна"

# Функция для входа в систему
def login(username, password):
    User = Query()
    user = user_db.search(User.username == username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')):  # Проверяем хешированный пароль
        return True
    return False

# Функция для получения данных пользователя
def get_user_data(token):
    try:
        url = "https://your-flowise-api.com/user"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Ошибка подключения: {e}")
        return None

# Функция для обновления профиля пользователя
def update_profile(token, new_username, new_email, new_password):
    try:
        url = "https://your-flowise-api.com/user"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"username": new_username, "email": new_email, "password": new_password}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        st.error(f"Ошибка подключения: {e}")
        return False

# Форма входа в систему
st.title("Вход в систему")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if login(username, password):
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.balance = 0  # Инициализация баланса
        st.success("Вы вошли в систему")
        switch_page("profile")
    else:
        st.error("Неправильный логин или пароль")

# Отображение личной информации пользователя
if "token" in st.session_state:
    st.title("Личный кабинет")
    user_data = get_user_data(st.session_state.token)
    if user_data:
        st.write(f"Username: {user_data['username']}")
        st.write(f"Email: {user_data['email']}")

        # Форма для редактирования профиля
        new_username = st.text_input("Новый username", value=user_data["username"])
        new_email = st.text_input("Новый email", value=user_data["email"])
        new_password = st.text_input("Новый пароль", type="password")
        confirm_password = st.text_input("Подтвердите пароль", type="password")

        if st.button("Сохранить"):
            if new_password != confirm_password:
                st.error("Пароли не совпадают")
            else:
                if update_profile(st.session_state.token, new_username, new_email, new_password):
                    st.success("Профиль обновлен")
                else:
                    st.error("Ошибка обновления профиля")
    else:
        st.error("Ошибка получения данных")

# Форма регистрации
st.title("Регистрация")
reg_username = st.text_input("Имя пользователя")
reg_email = st.text_input("Email")
reg_password = st.text_input("Пароль", type="password")
reg_confirm_password = st.text_input("Подтвердите пароль", type="password")

if st.button("Зарегистрироваться"):
    if reg_password != reg_confirm_password:
        st.error("Пароли не совпадают")
    else:
        success, message = register_user(reg_username, reg_email, reg_password)
        if success:
            st.success(message)
            st.session_state.username = reg_username
            st.session_state.authenticated = True
            st.session_state.balance = 0  # Инициализация баланса
            switch_page("app")
        else:
            st.error(message)
