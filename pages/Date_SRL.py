import streamlit as st

st.title('Încărcare Document Registrul Comertului')

# Creează un widget de încărcare a fișierului
uploaded_file = st.file_uploader("Trageți fișierul aici sau faceți clic pentru a încărca un document", type=["docx"])

if uploaded_file is not None:
  st.success("Fișier încărcat cu succes!")
  # Aici va fi adăugată logica de extracție a datelor din document
