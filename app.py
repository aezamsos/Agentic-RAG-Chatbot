import streamlit as st
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.response_agent import LLMResponseAgent
from utils.mcp import MCPMessage

st.set_page_config(page_title="Agentic RAG Chatbot", layout="wide")
st.title("🤖 Agentic RAG Chatbot")

uploaded_files = st.file_uploader("Upload your documents", type=['pdf', 'docx', 'pptx', 'csv', 'txt', 'md'], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Parsing documents..."):
        ingestion_agent = IngestionAgent()
        all_text = ingestion_agent.parse_documents(uploaded_files)

        retrieval_agent = RetrievalAgent()
        retrieval_agent.build_index(all_text)

        st.success("Documents parsed and indexed successfully!")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask a question about your documents")

if st.button("Ask") and user_query:
    with st.spinner("Retrieving answer..."):
        response_agent = LLMResponseAgent()
        retrieval_msg = retrieval_agent.retrieve(user_query)
        answer = response_agent.generate_answer(retrieval_msg)
        st.session_state.chat_history.append((user_query, answer))

if st.session_state.chat_history:
    st.subheader("Chat History")
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Bot:** {a}")
        st.markdown("---")