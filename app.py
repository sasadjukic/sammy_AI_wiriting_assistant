import streamlit as st
import ollama
import PyPDF2
from io import BytesIO
from system_prompt import SYSTEM_PROMPT
from styles import CUSTOM_CSS

MODEL = 'gemma3:4b'

def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            # For .txt files
            return uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            # For .pdf files
            try:
                pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.getvalue()))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            except Exception as e:
                return f"Error reading PDF: {e}"
    return None

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'assistant',
                'content': "Hi, I'm Sammy, your creative writing assistant. What great story are we going to write today?"
            }
        ]

def display_chat_history():
    for message in st.session_state.messages:
        if message["role"] != "system" and message["role"] != "hidden_content":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

def handle_user_input():
    if prompt := st.chat_input("What would you like to write about?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Sammy is thinking..."):
                response = ollama.chat(
                    model=MODEL,
                    messages=[
                        {"role": "user" if m["role"] == "hidden_content" else m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response_container = st.empty()
                full_response = ""
                for chunk in response:
                    full_response += chunk['message']['content']
                    response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def main():
    st.title("Sammy - AI Writing Assistant")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    initialize_session_state()

    # File uploader
    uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
    if uploaded_file is not None:
        file_content = process_uploaded_file(uploaded_file)
        if file_content:
            st.session_state.messages.append({"role": "hidden_content", "content": f"Document content:\n{file_content}"})
            st.success("File uploaded successfully! Sammy will consider its content.")

    display_chat_history()
    handle_user_input()

if __name__ == "__main__":
    main()
