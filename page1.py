import streamlit as st
import requests

API_URL = "https://flowise-renataraev64.amvera.io/api/v1/prediction/40d5e772-b471-411b-87fe-7a8cb397fd71"


def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
def show_page1():
    st.title("Page1")
    st.text("This is page RENAT")
    
    # Adding a chat functionality
    st.header("Chat with me!")
    user_input = st.text_input("Введите ваш вопрос", key="user_input_page1")
    char_counter = st.empty()  # Create an empty element to display the char count
    
    char_count = 0  # Initialize the char count
    if user_input:
        payload = {}  # Initialize payload
        if isinstance(user_input, set):
            payload["question"] = list(user_input)  # Convert set to list
        else:
            payload["question"] = user_input
        output = query(payload)
        response_text = output.get('text', '')
        st.write(response_text)

        # Update the char count
        char_count += len(response_text)
        char_counter.text(f"Character count: {char_count}")  # Display the updated char count

        # Store the response text for future updates
        if 'esponse_texts' not in st.session_state:
            st.session_state.response_texts = [response_text]
        else:
            st.session_state.response_texts.append(response_text)
        
        # Update the char count for all previous responses
        char_count = sum(len(text) for text in st.session_state.response_texts)
        char_counter.text(f"Character count: {char_count}")  # Display the updated char count