# pages/Plan_Afaceri.py
import streamlit as st

st.title('Încărcare Plan de Afaceri')

# Widget pentru încărcarea fișierului .docx
uploaded_file = st.file_uploader("Încărcați planul de afaceri modificat:", type=["docx"])

if uploaded_file is not None:
    st.success("Fișier încărcat cu succes!")
    # Aici poți adăuga logica pentru procesarea documentului încărcat
    # De exemplu, extragerea textului, identificarea placeholder-urilor etc.

