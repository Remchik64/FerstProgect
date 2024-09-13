import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from tinydb import TinyDB, Query
from yookassa import Configuration, Payment

# Проверка аутентификации
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.success("Вы не аутентифицированы. Пожалуйста, зарегистрируйтесь.")
    if st.button("Перейти к регистрации"):
        switch_page("registr")  # Перенаправление на страницу регистрации
    st.stop()

st.set_page_config(page_title="Оплата", layout="wide")

# Инициализация базы данных пользователей
user_db = TinyDB('user_database.json')

# Получение данных пользователя
User = Query()
user_data = user_db.search(User.username == st.session_state.username)[0]

# Инициализация атрибутов, если они не существуют
if "tokens_to_buy" not in st.session_state:
    st.session_state.tokens_to_buy = 0

if "rubles_to_pay" not in st.session_state:
    st.session_state.rubles_to_pay = 0

if "confirmation_url" not in st.session_state:
    st.session_state.confirmation_url = None

# Проверка и обновление баланса после возврата
if "balance" in st.session_state:
    user_data['balance'] = st.session_state.balance  # Обновление баланса пользователя

st.title("Страница оплаты")

# Отображение баланса
st.header("Баланс")
st.write(f"Ваш баланс: {round(user_data['balance'], 2)} рублей")

# Зона для покупки токенов
st.header("Покупка токенов")
tokens_to_buy = st.number_input("Количество токенов для покупки", min_value=1000, step=1000, key="tokens_to_buy_1")

# Конвертация токенов в рубли
def tokens_to_rubles(tokens):
    return tokens / 1500  # 1500 токенов = 1 рубль

rubles_to_pay = tokens_to_rubles(tokens_to_buy)

st.write(f"Сумма к оплате: {rubles_to_pay:.2f} рублей")

if st.button("Купить токены"):
    current_balance = user_data.get('balance', 0)
    if current_balance <= 0:
        st.error("Ваш баланс равен нулю. Пожалуйста, пополните баланс перед покупкой токенов.")
    else:
        if rubles_to_pay <= 0:
            st.error("Сумма к оплате должна быть больше нуля.")
        elif current_balance < rubles_to_pay:
            st.error("Недостаточно средств на балансе.")
        elif tokens_to_buy <= 0:  # Проверка на наличие токенов
            st.error("Количество токенов должно быть больше нуля.")
        else:
            
            # Обновление баланса
            new_balance = current_balance - rubles_to_pay
            user_db.update({'balance': new_balance}, User.username == st.session_state.username)
            st.session_state.balance = new_balance  # Сохранение нового баланса в session_state
            
            # Обновление количества токенов на счету пользователя
            current_tokens = user_data.get('tokens', 0)
            new_tokens = current_tokens + tokens_to_buy
            user_db.update({'tokens': new_tokens}, User.username == st.session_state.username)  # Обновление токенов
            
            # Обновление доступных символов
            st.session_state.available_symbols += tokens_to_buy * 1500  # 1500 символов на 1 токен
            
            # Создание платежа для покупки токенов
            payment = Payment.create({
                "amount": {
                    "value": rubles_to_pay,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://ferstprogect-4s6urffdveoebnwecknk7z.streamlit.app/payment"  # Замените на URL страницы оплаты
                },
                "description": "Покупка токенов"
            })
            
            # Перенаправление пользователя
            confirmation_url = payment.confirmation.confirmation_url
            st.experimental_set_query_params(redirect_url=confirmation_url)
            st.success(f"Перейдите по следующему URL для завершения платежа: {confirmation_url}")

# Зона для пополнения баланса
st.header("Пополнение баланса")
amount_to_add = st.number_input("Сумма для пополнения", min_value=0.01, step=10.0, key="amount_to_add_1")

if st.button("Пополнить баланс"):
    if amount_to_add <= 0:
        st.error("Сумма пополнения должна быть больше нуля.")
    else:
        # Создание платежа для пополнения баланса
        payment = Payment.create({
            "amount": {
                "value": amount_to_add,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://ferstprogect-4s6urffdveoebnwecknk7z.streamlit.app/payment"  # Замените на URL страницы оплаты
            },
            "description": "Пополнение баланса"
        })

        # Сохранение URL подтверждения в session_state
        st.session_state.confirmation_url = payment.confirmation.confirmation_url

# Проверка и отображение URL подтверждения, если он существует
if st.session_state.confirmation_url:
    st.write(f"URL для завершения платежа: {st.session_state.confirmation_url}")

# Настройка конфигурации YooKassa
shop_id = "452043"  # Ваш идентификатор магазина
secret_key = "test_98qixB_PszAZrKAwJkXnyVeUaTFLWQAjuVPUlPykZoU"  # Ваш секретный ключ

Configuration.configure(shop_id, secret_key)