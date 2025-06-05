
'''
import streamlit as st
from groq_api import ask_groq


# initialiser l'historique dans la session user

if "history" not in st.session_state:
    st.session_state.history = []


st.title("chatbot with Riabiation :")

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

            


'''
import os
import streamlit as st 
from groq_api import ask_groq
from db import init_db, get_or_create_user, get_history, save_message
from PyPDF2 import PdfReader
init_db()
if "history" not in st.session_state:
    st.session_state.history = []



# iniate database boot
st.title(" 🔐 Riabation Chatbot ")

# first step: User Connection

if "user_id" not in st.session_state:
    username = st.text_input("Put Your Username  :")
    if st.button("Connection") and username:
        user_id = get_or_create_user(username)
        st.write(f"user_id: {user_id}")
        st.session_state.user_id = user_id
        st.session_state.username = username
        st.session_state.history = get_history(user_id)
        st.success(f"Wellcome {username} !")



# Second Step chat interface 
if "user_id" in st.session_state:
    st.header(f"👤 Session : {st.session_state.username}")
    user_input = st.text_input("Tap Your Question to Riabation Intelij:")

    if st.button("Send") and user_input:
        #call groq with History
        response = ask_groq(user_input)

        #save in base
        save_message(st.session_state.user_id, "user", user_input)
        save_message(st.session_state.user_id, "assistant", response )

        # session update
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": response})
        st.write(type(st.session_state.history)) # for displaying class list

        # display History
        if st.session_state.history:
            st.subheader("💬 last Converstions")
            for msg in st.session_state.history:
                role = "🧑 You" if msg["role"] == "user" else "🤖 IA"
                st.markdown(f"**{role}** : {msg['content']}")




# PDF TXT FILE ANALYSE

st.subheader("📁 File Analyser")
upload_file = st.file_uploader("Upload A PDF & TXT & .chat File", type=["pdf", "txt", "chat"])


# initiate the text variable
text = ""
if upload_file:
    file_ext = os.path.splitext(upload_file.name)[1].lower()

    # reading the content of file
    # text = ""
    if file_ext == ".pdf":
        pdf = PdfReader(upload_file)
        for page in  pdf.pages:
            text += page.extract_text()
    elif file_ext in [".txt", ".chat"]:
        text = upload_file.read().decode("utf-8")




# display a plain text
st.text_area("📝 extracted content  :", text[:2000], height=200)

#resume
if st.button("📌 Summarize the File"):
    prompt_summary = f"Here is some text extracted from a file:\n\n{text[:5000]}\n\nMake a clear and concise summary."
    summary = ask_groq(prompt_summary)
    st.success("📋 Summary  :")
    st.write(summary)


# Information Extraction
if st.button("🔍  Extract important information :"):
    prompt_infos = f"Here is a text:\n\n{text[:5000]}\n\nHighlight the essential information or key points in the form of bullet points."
    points = ask_groq(prompt_infos)
    st.success("📌  Key points   ::")
    st.markdown(points)