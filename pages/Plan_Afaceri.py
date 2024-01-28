# pages/Plan_Afaceri.py
import streamlit as st
from docx import Document

def load_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n\n'.join(full_text)

# Calea către fișierul .docx în folderul assets
file_path = './assets/machetaPlan.docx'
docx_text = load_docx(file_path)

# Afișează textul într-o zonă editabilă și permite consultantului să facă modificări
editable_text = st.text_area("Editați textul după necesități:", value=docx_text, height=300)

# Buton pentru salvarea modificărilor
if st.button('Salvează Modificările'):
    # Aici poți adăuga logica pentru salvarea textului modificat
    # De exemplu, salvarea într-un nou document .docx sau într-o bază de date
    st.success("Modificările au fost salvate cu succes!")
