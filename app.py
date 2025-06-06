import os
import streamlit as st
from groq_api import ask_groq
from db import init_db, save_message
from PyPDF2 import PdfReader
from auth import login, signup  # Import des fonctions depuis auth.py
import hashlib
import sqlite3

# Initialiser la base de données
init_db()

# Initialiser l'historique dans la session utilisateur
if "history" not in st.session_state:
    st.session_state.history = []

# Menu principal
st.title("🔐 Riabation Chatbot")
menu = st.sidebar.selectbox("Menu", ["Se connecter", "Créer un compte"])

if "username" not in st.session_state:
    if menu == "Se connecter":
        login()  # Appel de la fonction login() depuis auth.py
    elif menu == "Créer un compte":
        signup()  # Appel de la fonction signup() depuis auth.py
else:
    # Page principale
    st.title("🔍 Page principale de recherche")
    st.header(f"👤 Session : {st.session_state.username}")

    # Interface de chat
    user_input = st.text_input("Posez votre question à Riabation :")
    if st.button("Envoyer") and user_input:
        # Appeler l'API Groq avec l'historique
        response = ask_groq(user_input)

        # Enregistrer dans la base de données
        save_message(st.session_state.user_id, "user", user_input)
        save_message(st.session_state.user_id, "assistant", response)

        # Mettre à jour l'historique dans la session
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": response})

        # Afficher l'historique
        if st.session_state.history:
            st.subheader("💬 Historique des conversations")
            for msg in st.session_state.history:
                role = "🧑 Vous" if msg["role"] == "user" else "🤖 IA"
                st.markdown(f"**{role}** : {msg['content']}")

    # Analyse de fichiers
    st.subheader("📁 Analyse de fichiers")
    upload_file = st.file_uploader("Téléchargez un fichier (PDF, TXT, .chat)", type=["pdf", "txt", "chat"])

    # Initialiser la variable texte
    text = ""
    if upload_file:
        file_ext = os.path.splitext(upload_file.name)[1].lower()

        # Lire le contenu du fichier
        if file_ext == ".pdf":
            pdf = PdfReader(upload_file)
            for page in pdf.pages:
                text += page.extract_text()
        elif file_ext in [".txt", ".chat"]:
            text = upload_file.read().decode("utf-8")

    # Afficher le contenu extrait
    st.text_area("📝 Contenu extrait :", text[:2000], height=200)

    # Résumé
    if st.button("📌 Résumer le fichier"):
        prompt_summary = f"Voici un texte extrait d'un fichier :\n\n{text[:5000]}\n\nFaites un résumé clair et concis."
        summary = ask_groq(prompt_summary)
        st.success("📋 Résumé :")
        st.write(summary)

    # Extraction d'informations importantes
    if st.button("🔍 Extraire les informations importantes"):
        prompt_infos = f"Voici un texte :\n\n{text[:5000]}\n\nMettez en évidence les informations essentielles sous forme de points clés."
        points = ask_groq(prompt_infos)
        st.success("📌 Points clés :")
        st.markdown(points)