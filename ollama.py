from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import ollama
import Streamlit as st

st.title("Geetha's show chat bot")
input_txt = st.text_input("please enter your queries here...")
prompt= ChatPromptTemplate.from_messages(
    [("system","you are a helpful ai assistant. your name is Geetha's assisant"),
     ("user" ,"user query:{query}")
    ])
llm = ollama(model = "llama2")
outputparser = StrOutputParser()
chain = prompt|llm|output_parser
if input_txt:
    str.write(chain.invoke({"query": input_txt}))