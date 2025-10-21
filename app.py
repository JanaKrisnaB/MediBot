import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Healthcare Chatbot", page_icon="🩺", layout="centered")
st.title("🩺 MediBot - Your Healthcare Assistant")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

SYSTEM_PROMPT = (
    "You are a kind and professional healthcare assistant. "
    "Provide general medical guidance and explanations for symptoms. "
    "Do NOT give strict diagnoses. Always remind users to consult a doctor."
)

# Display chat messages
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.chat_message("user").markdown(chat["content"])
    else:
        st.chat_message("assistant").markdown(chat["content"])

# User input
if prompt := st.chat_input("Describe your symptoms or ask a health-related question..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # Build messages for Gemini with history
            messages = [{"author": "system", "content": SYSTEM_PROMPT}]
            for msg in st.session_state.history:
                author = "user" if msg["role"] == "user" else "assistant"
                messages.append({"author": author, "content": msg["content"]})

            # Get Gemini response
            response = genai.chat.create(
                model="gemini-2.5-flash",
                messages=messages
            )
            reply = response.last
            st.chat_message("assistant").markdown(reply)
            st.session_state.history.append({"role": "assistant", "content": reply})

st.divider()
st.markdown("⚠️ **Disclaimer:** This chatbot provides general information and is not a substitute for professional medical advice. Always consult a qualified healthcare provider.")
