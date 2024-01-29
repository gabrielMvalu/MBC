# app.py
import streamlit as st

st.title("Pagina Principală")
st.write("Bine ați venit la aplicația multipagină!")

# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)
