import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Start a chat session (maintains history)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Streamlit App UI
st.set_page_config(page_title="💬 Gemini Chatbot", layout="centered")

st.title("🤖 Gemini Chatbot")
st.markdown("Ask me anything — powered by Google's Gemini 2.5 Flash!")

# Chat history display
for message in st.session_state.chat.history:
    role = "🧑 You" if message["role"] == "user" else "🤖 Gemini"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    with st.chat_message("🧑 You"):
        st.markdown(user_input)

    # Get Gemini response (streaming)
    with st.chat_message("🤖 Gemini"):
        message_placeholder = st.empty()
        full_response = ""
        response = st.session_state.chat.send_message(user_input, stream=True)

        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Save to session history
    st.session_state.chat.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.chat.history.append({"role": "model", "parts": [{"text": full_response}]})
