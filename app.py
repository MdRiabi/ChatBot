import streamlit as st
from groq_api import ask_groq


# initialiser l'historique dans la session user

if "history" not in st.session_state:
    st.session_state.history = []


st.title("chatbot with Groq")

user_input = st.text_input("please put your question to AI")

if st.button("send") and user_input:
    # call  the Grpq API with History
    response = ask_groq(user_input, st.session_state.history)

    # add the question and response in History
    st.session_state.history.append({"role":"user", "content":user_input})
    st.session_state.history.append({"role":"assistant", "content":response})


    #display the chat history

    if st.session_state.history:
        st.subheader("conversation History")
        for msg in st.session_state.history:
            role = "🧑you" if msg["role"] == "user" else "🤖 AI"
            st.markdown(f"**{role}** : {msg['content']}")
