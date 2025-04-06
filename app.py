import os
import sys
from datetime import datetime
import plotly.express as px
import requests
import streamlit as st
from src.backend.mongo_utils import fetch_data_from_mongo
import streamlit.components.v1 as components
from prebuilt_prompt.custom_data import handle_custom_logic
from prebuilt_prompt.business_queries import (
    total_sales, most_engaging_customer, most_popular_product, highest_sales_by_country)

from src.utils.relationship_builder import build_dataset_relationship
from src.visualizer.visualization import generate_visualization
st.set_page_config(page_title="BizBuddy AI", layout='centered')
st.sidebar.title("Data Analysis")
st.title("BizBuddy AI - Your Business Assistant")

BOT_NAME = "BizBuddy AI"
API_URL = "http://127.0.0.1:8000/chat/"


# Initializing session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get chatbot response


def get_response(message):
    message_lower = message.lower()

    custom_reply = handle_custom_logic(message)
    if custom_reply:
        return custom_reply

    response = requests.post(API_URL, json={"user_message": message})
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    return "Error: Unable to connect to the AI server."

# Define loading of custom css function


def load_css(file_name):
    with open(file_name, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Load the custom css
load_css("src/static/custom_style.css")


# Chat display
chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        # time_sent = msg["timestamp"]
        avatar_url = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png" if role == "bot" else "https://cdn-icons-png.flaticon.com/512/9131/9131529.png"
        align_class = "bot" if role == "bot" else "user"
        st.markdown(f"""
                <div class="chat-row {align_class}">
                {'<img src="'+ avatar_url +'" class="avatar">' if role=='bot' else ''}
                <div class="chat-bubble">{content}</div>

                {'<img src="'+avatar_url +'" class="avatar">' if role=='user' else ''}

              """, unsafe_allow_html=True)

# st.markdown("## 📊 Business Dashboard")
# if st.button("Show Dashboard"):
#     generate_visualization()
if st.session_state.get("trigger_visualization"):
    generate_visualization()
    st.session_state.trigger_visualization = False


# Input Section
st.markdown("---")
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Type your message", placeholder="Ask a business question......")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    current_time = datetime.now().strftime("%I:%M %p")

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
    })

    # Get reply from bot
    bot_reply = get_response(user_input)

    # Save the bot reply
    st.session_state.chat_history.append({
        "role": "bot",
        "content": bot_reply,

    })

    st.rerun()
