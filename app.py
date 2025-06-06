
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


# connexion page code 
'''
st.title("🔐 ChatBot ")

menu = st.sidebar.selectbox("Menu", ["Se connecter", "Créer un compte"])

if menu == "Créer un compte":
    new_user = st.text_input("Nom d'utilisateur")
    new_pass = st.text_input("Mot de passe", type="password")
    if st.button("Créer le compte"):
        if register_user(new_user, new_pass):
            st.success("Compte créé ! Connecte-toi maintenant.")
        else:
            st.error("❌ Ce nom d'utilisateur existe déjà.")
    

elif menu == "Se connecter":
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if verify_user(username, password):
            st.session_state["username"] = username
            st.success(f"Bienvenue {username} !")
        else:
            st.error("Identifiants invalides.")
        

# Bloquer l'accès s'il n'y a pas d'utilisateur
if "username" not in st.session_state:
    st.warning("Veuillez vous connecter.")

else:
    # Page principale
    st.title("🔍 Page principale de recherche")
    st.write("Bienvenue sur la page principale de recherche.")
    


# end connexion page code 

'''





import os
import streamlit as st 
from groq_api import ask_groq
from db import init_db, get_or_create_user, get_history, save_message
from PyPDF2 import PdfReader
import hashlib
import sqlite3



init_db()
if "history" not in st.session_state:
    st.session_state.history = []


#   Utility functions for authentication

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username =?",
        (username,)

    )
    row = cursor.fetchone()
    conn.close()

    if row and hash_password(password) == row[0]:
        return True
    return False


def register_user(username, password):
    try:
        conn = sqlite3.connect("history.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?,?)", (username, hash_password(password))

        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# END Utility functions for authentication






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