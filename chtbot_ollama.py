from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import ollama
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Geetha's Show Chatbot", layout="wide")

# Title
st.title("Geetha's Show Chatbot")

# Initialize session state for chat history and bot personality
if "history" not in st.session_state:
    st.session_state["history"] = []
if "personality" not in st.session_state:
    st.session_state["personality"] = "Friendly"

# Personality options
personality_options = {
    "Friendly": "You are a friendly and cheerful AI assistant.",
    "Professional": "You are a professional and concise AI assistant.",
    "Humorous": "You are a witty and humorous AI assistant."
}

# Sidebar for chatbot customization
st.sidebar.header("Customize Chatbot")
st.session_state["personality"] = st.sidebar.selectbox(
    "Choose the chatbot's personality:",
    list(personality_options.keys())
)

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state["history"] = []

# User input
input_txt = st.text_input("Please enter your queries here...")

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", personality_options[st.session_state["personality"]]),
        ("user", "User query: {query}")
    ]
)

# Initialize the LLM model
llm = ollama.Ollama(model="llama2")

# Output parser
output_parser = StrOutputParser()

# Chat processing
if input_txt:
    with st.spinner("Geetha's Assistant is thinking..."):
        # Construct the chain manually
        query_prompt = prompt.format(query=input_txt)
        response = llm(query_prompt)
        parsed_response = output_parser.parse(response)
        
        # Update chat history
        st.session_state["history"].append(("User", input_txt))
        st.session_state["history"].append(("Geetha's Assistant", parsed_response))

# Display chat history
if st.session_state["history"]:
    st.write("### Chat History")
    for sender, message in st.session_state["history"]:
        if sender == "User":
            st.write(f"**{sender}:** {message}")
        else:
            st.write(f"**{sender}:** {message}")

# Display a note in the sidebar
st.sidebar.info("Geetha's Assistant adapts based on the personality you choose!")
