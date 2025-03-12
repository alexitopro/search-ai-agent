import streamlit as st
from tramite_agent import agent_executor

def main():
    st.set_page_config(page_title = "Panda Agente 007")
    st.title("Panda Agente 007", anchor = False)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(placeholder = "Ingresa tu consulta sobre algún trámite académico de la Facultad de Ciencias e Ingeniería"):
        st.session_state.messages = []
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("Analizando tu consulta...", show_time=True):
            result = agent_executor.invoke({"input": prompt})
            response = result["output"]
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()