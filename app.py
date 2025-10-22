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
st.set_page_config(page_title="MediBot", layout="centered")

st.title("🤖 MediBot - Your HealthCare Assistant")
st.markdown("Ask me anything")

# Chat history display
for message in st.session_state.chat.history:
    role = "🧑 You" if message["role"] == "user" else "🤖 Gemini"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# User input
user_input = st.chat_input("Type your message here...")
prompt = f"Hey, you are a healthcare assistant. Respond accordingly and professionally.\nUser: {user_input}"
if user_input:
    # Display user message
    with st.chat_message("🧑 You"):
        st.markdown(user_input)

    # Get Gemini response (streaming)
    with st.chat_message("🤖 Gemini"):
        message_placeholder = st.empty()
        full_response = ""
        response = st.session_state.chat.send_message(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Save to session history
    st.session_state.chat.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.chat.history.append({"role": "model", "parts": [{"text": full_response}]})
