import ollama
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from chat_app.config import config
from chat_app.logger import get_logger

logger = get_logger(__name__)


def sidebar():
    with st.sidebar:
        st.selectbox("Select Database provider", ["sqlite3"])


def session_state_init():
    configs = config.get()

    if "selected_model" not in st.session_state:
        if configs:
            st.session_state["selected_model"] = configs.selected_model
            if not configs.selected_model:
                st.session_state["selected_model_index"] = None
            else:
                st.session_state["selected_model_index"] = get_ollama_models().index(
                    configs.selected_model
                )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            AIMessage("How can I help you?"),
        ]

    if "user_input_disabled" not in st.session_state:
        st.session_state["user_input_disabled"] = False


@st.cache_data
def get_ollama_models() -> list[str]:
    models_list = ollama.list()
    if not models_list:
        return ["Unknown"]

    payload = []
    for model in models_list["models"]:
        payload.append(model["name"])

    return payload


def disable():
    st.session_state.user_input_disabled = True


def call_llm(messages: list):
    logger.info(f"Using model: {st.session_state['selected_model']}")

    llm = ChatOllama(
        model=st.session_state["selected_model"],
        disable_streaming=False,
    )
    msgs = ChatPromptTemplate.from_messages(messages)
    chain = msgs | llm | StrOutputParser()
    return chain.stream({})


def run():
    st.set_page_config(page_title="Personal Chatbot", initial_sidebar_state="collapsed")
    config._config_file_init()
    session_state_init()
    st.title(":material/chat: Personal :blue[Chatbot]")
    sidebar()

    _, col2 = st.columns(2)
    with col2:
        selected_model = st.selectbox(
            "Select model:",
            get_ollama_models(),
            help="Select a model to use for conversation",
            index=st.session_state["selected_model_index"],
        )
        if selected_model:
            config.write("selected_model", selected_model)
            st.session_state["selected_model"] = selected_model
    messages = st.session_state.messages
    for msg in messages:
        if isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)

        if isinstance(msg, HumanMessage):
            st.chat_message("human").write(msg.content)

    user_input = st.chat_input(
        placeholder="Write a message",
        disabled=st.session_state.user_input_disabled,
        on_submit=disable,
    )

    if user_input:
        messages.append(HumanMessage(user_input))
        st.chat_message("human").write(user_input)
        st.session_state.input_disabled = True
        res = call_llm(messages)
        with st.chat_message("assistant"):
            output = st.write_stream(res)

        messages.append(AIMessage(output))
        st.session_state.user_input_disabled = False
        st.rerun()
