import os
import sys
import pandas as pd
from datetime import datetime
import plotly.express as px
import requests
import streamlit as st
from prebuilt_prompt.custom_data import handle_custom_logic
from prebuilt_prompt.business_queries import handle_business_query, analyze_data_for_suggestions, handle_business_suggestion
from src.backend.mongo_utils import fetch_data_from_mongo
from src.visualizer.visualization import generate_visualization
from typing import Literal
from dataclasses import dataclass
import openai


@dataclass
class Message:
    role: Literal['user', 'bot']
    content: str
    timestamp: str
    analysis_needed: bool = False


openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="BizBuddy AI", layout='centered')
st.sidebar.title("Data Analysis")
st.title("BizBuddy AI - Your Business Assistant")

BOT_NAME = "BizBuddy AI"
API_URL = "http://127.0.0.1:8000/chat/"


# Initializing session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "bot",
        "content": "Hello! I am Bizbuddy AI. How can I assist your business today?",
        "analysis_needed": False
    }]


# Function to get chatbot response
def get_response(message: str) -> str:
    message_lower = message.lower()

    last_msg = st.session_state.chat_history[-1] if st.session_state.chat_history else None
    if last_msg and last_msg.get("analysis_needed", False) and "yes" in message_lower:
        # return handle_follow_up_analysis(last_msg.get("content", ""))
        return {
            "role": "bot",
            "content": handle_follow_up_analysis(last_msg.get("content", "")),
            "analysis_needed": False
        }

    custom_reply = handle_custom_logic(message_lower)
    if custom_reply:
        return custom_reply

    business_reply = handle_business_query(message_lower)
    if business_reply:
        return business_reply

    business_suggestions = analyze_data_for_suggestions(message_lower)
    if business_suggestions:
        return business_suggestions

    handle_business_suggestion_reply = handle_business_suggestion(
        message_lower)
    if handle_business_suggestion_reply:
        return handle_business_suggestion_reply

    response = requests.post(API_URL, json={"user_message": message})
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    return "Error: Unable to connect to the AI server."


def handle_follow_up_analysis(previous_message: str) -> str:
    """Handle follow-up requests for deeper analysis"""
    if "sales report" in previous_message.lower():
        st.session_state.trigger_visualization = True
        return "Here's the detailed sales dashboard. What specific aspect would you like to discuss?"

    if "detailed feedback" in previous_message.lower():
        reviews_df = pd.DataFrame(fetch_data_from_mongo("reviews"))
        negative_feedback = reviews_df[reviews_df["rating"] < 3]
        if not negative_feedback.empty:
            issues = negative_feedback["comments"].value_counts().head(
                3).index.tolist()
            return f"Main areas for improvement:\n\n- " + "\n- ".join(issues)
        return "Great news! No significant negative feedback found recently."
    return "I'll analyze this further. Please give me a moment...."


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
        content = msg["content"]
        role = msg["role"]

        avatar_url = "https://cdn-icons-png.flaticon.com/512/4712/4712109.png" if role == "bot" else "https://cdn-icons-png.flaticon.com/512/9131/9131529.png"
        align_class = "bot" if role == "bot" else "user"
        st.markdown(f"""
                <div class="chat-row {align_class}">
                {'<img src="'+ avatar_url +'" class="avatar">' if role=='bot' else ''}
                <div class="chat-bubble">{content}</div>

                {'<img src="'+avatar_url +'" class="avatar">' if role=='user' else ''}

              """, unsafe_allow_html=True)


# show dashboard if triggered
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
        "analysis_needed": False
    })

    # Get reply from bot
    bot_reply = get_response(user_input)

    # Save the bot reply
    st.session_state.chat_history.append({
        "role": "bot",
        "content": bot_reply,

    })

    st.rerun()
