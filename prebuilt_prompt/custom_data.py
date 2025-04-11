BOT_NAME = "BizBuddy AI"
DEVELOPER_NAME = "Shushil Shah"


def handle_custom_logic(message: str) -> str | None:
    message_lower = message.lower()

    if "your name" in message_lower or "who are you" in message_lower:
        return f"I am {BOT_NAME}!, your AI business assistant."

    if "who built you" in message_lower or "who created you" in message_lower:
        return f"I was created by {DEVELOPER_NAME}, a software engineer and data scientist."

    if "what can you do" in message_lower or "what are your capabilities" in message_lower:
        return f"I can assist you with data analysis, visualization, and answering business-related queries related to your dataset."

    if "show me the dashboard" in message_lower or "business insights" in message_lower:
        import streamlit as st
        st.session_state.trigger_visualization = True
        return "Here's the dashboard with latest insights."

    # Fallback for unknown business questions
    if any(word in message_lower for word in ["dashboard", "insights", "report", "analysis", "visualization"]):
        import streamlit as st
        st.session_state.trigger_visualization = True

        # Determine which tab to open based on context
        if "sales" in message_lower:
            st.session_state.dashboard_tab = "Sales"
        elif "review" in message_lower or "rating" in message_lower:
            st.session_state.dashboard_tab = "Reviews"
        elif "customer" in message_lower:
            st.session_state.dashboard_tab = "Customers"
        elif "support" in message_lower or "ticket" in message_lower:
            st.session_state.dashboard_tab = "Support"

        return "Here's the dashboard with the latest insights. What would you like to focus on?"
