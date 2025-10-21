import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit page setup
st.set_page_config(page_title="Healthcare Chatbot", page_icon="🩺", layout="centered")

st.title("🩺 AI Healthcare Chatbot")
st.caption("💬 I'm here to provide **general health information** — not a replacement for a doctor.")

# System prompt
SYSTEM_PROMPT = (
    "You are a kind and professional healthcare assistant. "
    "Provide general medical information, healthy lifestyle advice, "
    "and explanations for symptoms. "
    "Do NOT give strict diagnoses or prescribe medications. "
    "Always remind users to consult a doctor for confirmation."
)

# Maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I assist you today? 😊"}]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# User input
if prompt := st.chat_input("Describe your symptoms or ask a health-related question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your input..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

st.divider()
st.markdown("⚠️ **Disclaimer:** This chatbot provides general information and is not a substitute for professional medical advice. Always consult a qualified healthcare provider.")
