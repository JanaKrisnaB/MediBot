import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Streamlit UI
st.set_page_config(page_title="MediBot", layout="centered")
st.title("🤖 MediBot - Your Healthcare Assistant")
st.markdown("Ask me anything about your health concerns!")

# Display chat history
for message in st.session_state.chat.history:
    role = "🧑 You" if message.role == "user" else "🤖 MediBot"
    with st.chat_message(role):
        if message.parts:
            st.markdown(message.parts[0].text)

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Combine user message with context
    prompt = (
        "You are MediBot, a professional healthcare assistant. "
        "Respond in a helpful, empathetic, and medically accurate way. "
        f"User: {user_input}"
    )

    # Display user message
    with st.chat_message("🧑 You"):
        st.markdown(user_input)

    # Stream response
    with st.chat_message("🤖 MediBot"):
        message_placeholder = st.empty()
        full_response = ""
        response = st.session_state.chat.send_message(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
