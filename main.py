import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from loguru import logger
from openai import OpenAI

load_dotenv()

logger.info(os.getenv('GROQ_API_KEY'))

qclient = Groq()
client = OpenAI()

st.title('LLM CHAT')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for messages in st.session_state.messages:
    with st.chat_message(messages['role']):
        st.markdown(messages['content'])


def process_data(chat_completion) -> str:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content: yield chunk.choices[0].delta.content


if prompt := st.chat_input('Insert questions'):
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        stream_response = qclient.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You will only answer in Spanish, I gonna put a pdf an you gonna give me a summary",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="llama3-8b-8192",
            # model="gpt-4o-mini",
            stream=True
        )

        response = process_data(stream_response)

        response = st.write_stream(response)

    st.session_state.messages.append({'role': 'asistant', 'content': response})

    # print(chat_completion.choices[0].message.content)
    #fetch conectar el front con el back
