from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import ollama
import streamlit as st
import time

# Page Configuration
st.set_page_config(page_title="Geetha's Show Chatbot", layout="centered")

# CSS for custom styling
st.markdown(
    """
    <style>
    .chat-bubble {
        padding: 10px 15px;
        margin: 10px 0;
        border-radius: 10px;
        max-width: 70%;
    }
    .user {
        background-color: #dcf8c6;
        text-align: left;
        margin-left: auto;
    }
    .assistant {
        background-color: #f1f0f0;
        text-align: left;
        margin-right: auto;
    }
    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Animated welcome message
if "welcome_shown" not in st.session_state:
    st.session_state["welcome_shown"] = True
    with st.spinner("Initializing Geetha's Assistant..."):
        time.sleep(2)
    st.success("Geetha's Assistant is ready to chat! 🤖")

# Title with an emoji
st.title("🌟 Geetha's Show Chatbot 🌟")

# Initialize session state for history and personality
if "history" not in st.session_state:
    st.session_state["history"] = []
if "personality" not in st.session_state:
    st.session_state["personality"] = "Friendly"

# Sidebar customization
st.sidebar.header("Customize Your Chatbot")

# Theme selection
theme = st.sidebar.radio("Choose a theme:", ["Light", "Dark"], index=0)
if theme == "Dark":
    st.markdown(
        """
        <style>
        body { background-color: #121212; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Personality selection
personality_options = {
    "Friendly": "You are a friendly and cheerful AI assistant.",
    "Professional": "You are a professional and concise AI assistant.",
    "Humorous": "You are a witty and humorous AI assistant."
}
st.session_state["personality"] = st.sidebar.selectbox(
    "Select the chatbot's personality:",
    list(personality_options.keys())
)

# Clear history button
if st.sidebar.button("Clear Chat History"):
    st.session_state["history"] = []

# Export conversation history
if st.sidebar.button("Export Chat"):
    with open("chat_history.txt", "w") as file:
        for sender, message in st.session_state["history"]:
            file.write(f"{sender}: {message}\n")
    st.sidebar.success("Chat history exported!")

# User input
input_txt = st.text_input("💬 Type your message:")

# Define the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", personality_options[st.session_state["personality"]]),
        ("user", "User query: {query}")
    ]
)

# Initialize LLM model
llm = ollama.Ollama(model="llama2")

# Output parser
output_parser = StrOutputParser()

# Chat processing
if input_txt:
    with st.spinner("Geetha's Assistant is thinking..."):
        query_prompt = prompt.format(query=input_txt)
        response = llm(query_prompt)
        parsed_response = output_parser.parse(response)

        # Update history
        st.session_state["history"].append(("User", input_txt))
        st.session_state["history"].append(("Geetha's Assistant", parsed_response))

# Display chat history
st.write("### Conversation")
for sender, message in st.session_state["history"]:
    if sender == "User":
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-end;">
                <div class="chat-bubble user">{message}</div>
                <img src="https://via.placeholder.com/50/0000FF/808080?text=U" class="avatar" alt="User">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-start;">
                <img src="https://via.placeholder.com/50/FF0000/FFFFFF?text=A" class="avatar" alt="Assistant">
                <div class="chat-bubble assistant">{message}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Add a footer
st.markdown(
    """
    <hr>
    <div style="text-align: center;">
        🤖 Powered by Geetha's Assistant | <a href="#">Feedback</a>
    </div>
    """,
    unsafe_allow_html=True,
)
