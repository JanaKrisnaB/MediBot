import streamlit as st
from google.generativeai import genai
import os

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🩺 Healthcare Chatbot")

SYSTEM_PROMPT = (
    "You are a kind and professional healthcare assistant. "
    "Provide general guidance, explanations of symptoms, and healthy lifestyle tips. "
    "Do NOT give strict diagnoses. Always remind users to consult a doctor."
)

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for chat in st.session_state.history:
    role = "user" if chat["role"] == "user" else "assistant"
    st.chat_message(role).markdown(chat["content"])

# User input
if prompt := st.chat_input("Describe your symptoms or ask a question..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Combine all history for context
    messages = SYSTEM_PROMPT + "\n"
    for msg in st.session_state.history:
        author = "User" if msg["role"] == "user" else "Assistant"
        messages += f"{author}: {msg['content']}\n"

    # Get response from Gemini 2.5 Flash
    response = client.models.generate_text(
        model="gemini-2.5-flash",
        prompt=messages,
        max_output_tokens=500
    )
    reply = response.output_text
    st.chat_message("assistant").markdown(reply)
    st.session_state.history.append({"role": "assistant", "content": reply})

st.divider()
