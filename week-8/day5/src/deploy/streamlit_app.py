import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="HR Assistant", layout="centered")

st.title("💼 HR Assistant Chatbot")


temperature = 0.7
top_p = 0.9
top_k = 40

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# DISPLAY CHAT
# -----------------------------
for chat in st.session_state.history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# -----------------------------
# INPUT
# -----------------------------
user_input = st.chat_input("Ask something about HR...")

if user_input:
    payload = {
        "message": user_input,
        "history": st.session_state.history,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.text(response.text)
        else:
            result = response.json()
            reply = result["response"]

            st.session_state.history.append({"role": "user", "content": user_input})
            st.session_state.history.append({"role": "assistant", "content": reply})

            st.rerun()

    except Exception as e:
        st.error(f"Request failed: {e}")