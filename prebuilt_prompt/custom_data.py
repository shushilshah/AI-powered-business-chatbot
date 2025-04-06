BOT_NAME = "BizBuddy AI"


def handle_custom_logic(message: str) -> str | None:
    message_lower = message.lower()

    if "your name" in message_lower or "who are you" in message_lower:
        return f"I am {BOT_NAME}!, your AI business assistant."

    if "who built you" in message_lower or "who created you" in message_lower:
        return f"I was created by Shushil Shah, a software engineer and data scientist."

    if "what can you do" in message_lower or "what are your capabilities" in message_lower:
        return f"I can assist you with data analysis, visualization, and answering business-related queries related to your dataset."

    if "show dashboard" in message_lower:
        import streamlit as st
        st.session_state.trigger_visualization = True
        return "Here's the dashboard with latest insights."
    return None
