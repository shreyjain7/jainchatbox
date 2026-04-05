import streamlit as st
import ollama
import json
import os
import uuid

st.set_page_config(page_title="Jain Chat Box", layout="wide")

DATA_FILE = "chats.json"

# -------- Load Data --------


def load_knowledge():
    if os.path.exists("jain_knowledge.txt"):
        with open("jain_knowledge.txt", "r") as f:
            return f.read()
    return ""

knowledge = load_knowledge()


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
            "content": "You are Jain Chat Box, a smart AI assistant. Answer clearly. If user asks about Jainism, answer respectfully and accurately. Also help with general questions."
        }
    ]
    save_chats(chats)
    st.session_state.chat_id = chat_id

# Initialize chat_id
if "chat_id" not in st.session_state:
    if chats:
        st.session_state.chat_id = list(chats.keys())[0]
    else:
        chat_id = str(uuid.uuid4())
        chats[chat_id] = [
            {
                "role": "system",
                "content": "You are Jain Chat Box, a smart AI assistant. Answer clearly. If user asks about Jainism, answer respectfully and accurately. Also help with general questions."
            }
        ]
        save_chats(chats)
        st.session_state.chat_id = chat_id

# Sidebar chat list
for cid in chats.keys():
    if st.sidebar.button(f"Chat {cid[:6]}"):
        st.session_state.chat_id = cid

# -------- Current Chat --------
messages = chats[st.session_state.chat_id]

st.title("🧠 Jain Chat Box")

# -------- Quick Jain Questions --------
st.subheader("📿 Jain Quick Questions")

col1, col2, col3 = st.columns(3)

if col1.button("What is Jainism?"):
    st.session_state.quick = "What is Jainism?"

if col2.button("Who was Mahavira?"):
    st.session_state.quick = "Who was Mahavira?"

if col3.button("What are Jain principles?"):
    st.session_state.quick = "What are Jain principles?"

# Display messages
for msg in messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Input
user_input = st.chat_input("Ask anything...")

# Handle quick question
if "quick" in st.session_state:
    user_input = st.session_state.quick
    del st.session_state.quick

if user_input:
    messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ollama.chat(
                model="llama3",
                messages=messages
            )
            reply = response['message']['content']
            st.write(reply)

    messages.append({"role": "assistant", "content": reply})

    chats[st.session_state.chat_id] = messages
    save_chats(chats)


    {
 "role": "system",
 "content": "You are Jain Chat Box, an expert in Jainism. Answer deeply about Jain philosophy, Mahavira, principles like Ahimsa, Anekantavada, Aparigraha. Also help with general questions."
}
    
col1, col2, col3 = st.columns(3)

if col1.button("What is Ahimsa?"):
    st.session_state.quick = "Explain Ahimsa in Jainism"

if col2.button("What is Anekantavada?"):
    st.session_state.quick = "Explain Anekantavada"

if col3.button("What are 5 vows?"):
    st.session_state.quick = "Explain the 5 vows of Jainism"

