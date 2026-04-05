import streamlit as st
from openai import OpenAI
import json
import os
import uuid

# -------- API Setup --------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Jain Chat Box", layout="wide")

DATA_FILE = "chats.json"

# -------- Load Knowledge --------
def load_knowledge():
    if os.path.exists("jain_knowledge.txt"):
        with open("jain_knowledge.txt", "r") as f:
            return f.read()
    return ""

knowledge = load_knowledge()

# -------- Load Chats --------
def load_chats():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chats(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

chats = load_chats()

# -------- Sidebar --------
st.sidebar.title("💬 Jain Chat Box")

if st.sidebar.button("➕ New Chat"):
    chat_id = str(uuid.uuid4())
    chats[chat_id] = [
        {
            "role": "system",
            "content": f"""
You are Jain Chat Box, an expert in Jainism.

Use this knowledge:
{knowledge}

Answer deeply about Jain philosophy, Mahavira, Ahimsa, Anekantavada, Aparigraha.
Also help with general questions.
"""
        }
    ]
    save_chats(chats)
    st.session_state.chat_id = chat_id

# -------- Initialize Chat --------
if "chat_id" not in st.session_state:
    if chats:
        st.session_state.chat_id = list(chats.keys())[0]
    else:
        chat_id = str(uuid.uuid4())
        chats[chat_id] = [
            {
                "role": "system",
                "content": f"""
You are Jain Chat Box, an expert in Jainism.

Use this knowledge:
{knowledge}

Answer clearly and respectfully.
"""
            }
        ]
        save_chats(chats)
        st.session_state.chat_id = chat_id

# -------- Sidebar Chat List --------
for cid in chats.keys():
    if st.sidebar.button(f"Chat {cid[:6]}"):
        st.session_state.chat_id = cid

messages = chats[st.session_state.chat_id]

# -------- UI --------
st.title("🧠 Jain Chat Box")

# -------- Quick Questions --------
st.subheader("📿 Jain Quick Questions")

col1, col2, col3 = st.columns(3)

if col1.button("What is Jainism?"):
    st.session_state.quick = "Explain Jainism"

if col2.button("Who was Mahavira?"):
    st.session_state.quick = "Who was Mahavira?"

if col3.button("What are Jain principles?"):
    st.session_state.quick = "Explain Jain principles"

col4, col5, col6 = st.columns(3)

if col4.button("What is Ahimsa?"):
    st.session_state.quick = "Explain Ahimsa in Jainism"

if col5.button("What is Anekantavada?"):
    st.session_state.quick = "Explain Anekantavada"

if col6.button("What are 5 vows?"):
    st.session_state.quick = "Explain the 5 vows of Jainism"

# -------- Display Messages --------
for msg in messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# -------- Input --------
user_input = st.chat_input("Ask anything...")

# Handle quick questions
if "quick" in st.session_state:
    user_input = st.session_state.quick
    del st.session_state.quick

# -------- AI Response --------
if user_input:
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )
            reply = response.choices[0].message.content
            st.write(reply)

    messages.append({"role": "assistant", "content": reply})

    chats[st.session_state.chat_id] = messages
    save_chats(chats)
