import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
You are MediBot — a helpful, empathetic, and knowledgeable healthcare assistant.
Your job is to:
- Help users understand their symptoms, diseases, medications, and health conditions in simple terms.
- Provide safe, factual, and evidence-based medical guidance.
- Encourage users to seek professional care when needed.
- NEVER provide direct medical diagnosis, prescriptions, or emergency instructions.
- Maintain a kind, supportive, and respectful tone like a real healthcare professional.
"""

# Initialize session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[
        {"role": "system", "parts": [{"text": SYSTEM_PROMPT}]}
    ])

# Streamlit UI
st.set_page_config(page_title="🩺 MediBot", layout="centered")
st.title("🤖 MediBot - Your Healthcare Assistant")
st.markdown("I’m here to help you understand your health better. How can I assist you today?")

for message in st.session_state.chat.history[1:]:
    role = "🧑 You" if message["role"] == "user" else "🤖 MediBot"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# User input
user_input = st.chat_input("Describe your symptoms or ask a health question...")

if user_input:
    # Show user message
    with st.chat_message("🧑 You"):
        st.markdown(user_input)

    # Generate MediBot response (streamed)
    with st.chat_message("🤖 MediBot"):
        message_placeholder = st.empty()
        full_response = ""
        response = st.session_state.chat.send_message(user_input, stream=True)

        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Update chat history
    st.session_state.chat.history.append({"role": "user", "parts": [{"text": user_input}]})
    st.session_state.chat.history.append({"role": "model", "parts": [{"text": full_response}]})
