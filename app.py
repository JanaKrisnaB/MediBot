import streamlit as st
import google.generativeai as genai
import os

# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🩺 MediBot - Your Healthcare Assistant")

user_input = st.text_input("Describe your symptoms or ask a question:")

if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing..."):
            response = genai.chat.create(
                model="gemini-1.5",
                messages=[
                    {"author": "system", "content": (
                        "You are a kind and professional healthcare assistant. "
                        "You provide general medical guidance and explanations for symptoms, "
                        "but never give strict diagnoses. Always remind users to consult a doctor."
                    )},
                    {"author": "user", "content": user_input}
                ]
            )
            st.success("Here’s what I think:")
            st.write(response.last)
