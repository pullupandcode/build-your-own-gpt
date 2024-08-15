""" using streamlit to create a UI """

import logging
import streamlit as st
from streamlit_chat import message
from langchain_community.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

BASE_URL = "http://localhost:11434"


logging.basicConfig(level=logging.INFO)

def display_messages():
    """ display your chat messages """
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def process_input():
    """ process user input for chat """
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner("Thinking"):
            agent_text = st.session_state["assistant"].invoke({'question': user_text})

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))

def create_agent(model):
    """ Function to stream chat response based on selected model """

    llm = Ollama(model=model, base_url=BASE_URL)


    prompt = PromptTemplate.from_template(
        """
            You are a senior engineer, helping someone who is learning how to code.
            Answer thieir following question: {question}
        """
    )

    chain = prompt | llm | StrOutputParser()
    return chain

def main():
    """ main """
    if len(st.session_state) == 0:
        st.session_state["user_input"] = ""
        st.session_state["messages"] = []
        st.session_state["assistant"] = create_agent('llama3')


    st.title("My Programming Tutor")  # Set the title of the Streamlit app
    logging.info("App started")  # Log that the app has started

    # Sidebar for model selection
    # model = st.sidebar.selectbox("Choose a model", ["llama3", "phi3", "mistral"])
    # logging.info(f"Model selected: {model}")

    display_messages()

    # Prompt for user input and save to chat history
    st.text_input("Enter your programming question", key='user_input', on_change=process_input)


if __name__ == "__main__":
    main()
