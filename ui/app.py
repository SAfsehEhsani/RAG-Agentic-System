import streamlit as st
import os
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from agent import agent 

st.set_page_config(page_title="Federal Registry RAG Agent")

st.title("US Federal Registry RAG Agent")
st.write("Ask me questions about recent US federal documents like executive orders, rules, or notices. Data is simulated and updated via a daily pipeline.")
st.write("Example queries:")
st.write("- `What are the recent executive orders?`")
st.write("- `Are there any documents related to AI security?`")
st.write("- `Tell me about recent documents from the EPA.`")

if "messages" not in st.session_state:
    st.session_state.messages = [] 

for message in st.session_state.messages:
    
    if message["role"] in ["user", "assistant"]:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    

if prompt := st.chat_input("Ask a question about federal documents..."):
    
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.spinner("Thinking..."): 
         agent_response = agent.chat_with_agent(prompt, st.session_state.messages)

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
         with st.chat_message("assistant", avatar="🤖"):
             st.markdown(st.session_state.messages[-1]["content"])
