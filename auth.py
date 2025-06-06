import streamlit as st
from db import get_or_create_user, get_history, register_user, verify_user

def login():
    """Gère la connexion de l'utilisateur."""
    st.subheader("🔑 Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        if verify_user(username, password):
            st.session_state["username"] = username
            st.session_state["user_id"] = get_or_create_user(username)
            st.session_state.history = get_history(st.session_state["user_id"])
            st.success(f"Bienvenue {username} !")
            st.experimental_rerun()
        else:
            st.error("Identifiants invalides.")

def signup():
    """Gère la création de compte."""
    st.subheader("📝 Création de compte")
    new_user = st.text_input("Nom d'utilisateur")
    new_pass = st.text_input("Mot de passe", type="password")
    if st.button("Créer le compte"):
        if register_user(new_user, new_pass):
            st.success("Compte créé avec succès ! Connectez-vous maintenant.")
            st.experimental_rerun()
        else:
            st.error("❌ Ce nom d'utilisateur existe déjà.")