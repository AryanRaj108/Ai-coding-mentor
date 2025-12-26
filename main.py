import streamlit as st
from api import get_mentor_response, GEMINI_API_KEY

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-right: 2px solid #e0e0e0;
    }
    .chat-message-user {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .chat-message-assistant {
        background-color: #28a745;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .history-item {
        padding: 8px;
        border-bottom: 1px solid #e0e0e0;
        font-size: 14px;
        cursor: pointer; /* Clickable */
    }
    .history-item:hover {
        background-color: #f5f5f5; /* Hover effect */
    }
    .full-width-header {
        width: 100%;
        margin-top: 60px;
        position: fixed;
        top: 0;
        left: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        padding-left: 350px;
        background-color: rgb(38, 39, 48);
        z-index: 1000;
        box-sizing: border-box;
        height: 60px; /* Ensure a fixed height */
    }
    .header-left {
        display: flex;
        align-items: center;
    }
    .header-left img {
        width: 40px;
        height: 40px;
        margin-right: 10px;
    }
    .header-left h1 {
        font-size: 24px;
        margin: 0;
        color: #ffffff; /* Changed to white for contrast */
    }
    .header-right {
        font-size: 16px;
        color: #ffffff; /* Changed to white for contrast */
    }
    .stApp {
        padding-top: 80px; /* Adjust for header height */
    }
    .new-chat-btn {
        background-color: #007bff;
        color: white;
        padding: 8px;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
        margin-bottom: 10px; /* Space below button */
    }
    .new-chat-btn:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# Full-Width Header Section
st.markdown("""
    <div class="full-width-header">
        <div class="header-left">
            <img src="https://play-lh.googleusercontent.com/neTZPbKq8VdqPzzo5lORxvPRlTrSYoqRTF9qUuc4FWa4WTo1tpdcpiHb2FPD4DCs6Q=w480-h960-rw" alt="Logo">
            <h1>Code AI</h1>
        </div>
        <div class="header-right">
            Developed by Pratyush Panda, Aryan raj, Amarnath.
        </div>
    </div>
""", unsafe_allow_html=True)

# Streamlit UI
st.markdown("### ✨ AI Coding Mentor Chatbot ✨")

# Sidebar: New Chat and Chat History
with st.sidebar:
    # New Chat Button
    if st.button("New Chat", key="new_chat"):
        st.session_state.current_messages = []  # Clear only the current chat display

    # Chat History Section
    st.subheader("📜 Chat History")
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Full history
    if "current_messages" not in st.session_state:
        st.session_state.current_messages = []  # Current chat display

    # Display history items as clickable lines
    for i, message in enumerate(st.session_state.messages):
        role_icon = "👤" if message["role"] == "user" else "🤖"
        if st.button(f"{role_icon} {message['content'][:50]}{'...' if len(message['content']) > 50 else ''}", key=f"history_{i}"):
            # Display selected message and remove it from history
            st.session_state.current_messages = [message]
            st.session_state.messages.pop(i)

# Main Chat Area
st.markdown("### 💬 Chat with Your Mentor")
chat_container = st.container()

# Display current messages
with chat_container:
    for message in st.session_state.current_messages:
        if message["role"] == "user":
            st.markdown(f"<div class='chat-message-user'>👤 You: {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message-assistant'>🤖 Mentor: {message['content']}</div>", unsafe_allow_html=True)

# User input
user_input = st.chat_input("Ask a coding question...")
if user_input:
    # Add user message to current display and full history
    st.session_state.current_messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with chat_container:
        st.markdown(f"<div class='chat-message-user'>👤 You: {user_input}</div>", unsafe_allow_html=True)

    # Fetch and display mentor response only if non-empty
    if GEMINI_API_KEY:
        response = get_mentor_response(user_input)
        if response:  # Only add and display if response is non-empty
            st.session_state.current_messages.append({"role": "assistant", "content": response})
            st.session_state.messages.append({"role": "assistant", "content": response})
            with chat_container:
                st.markdown(f"<div class='chat-message-assistant'>🤖 Mentor: {response}</div>", unsafe_allow_html=True)
    else:
        st.error("Gemini API key not set. Please configure GEMINI_API_KEY in api.py.")