# pages/Plan_Afaceri.py
import streamlit as st
from docx import Document

def load_docx(file_path):
    # Încarcă documentul .docx
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:  # Iterează prin fiecare paragraf
        full_text.append(para.text)  # Adaugă textul paragrafului la lista de text
    return '\n'.join(full_text)  # Întoarce textul complet ca un singur string

# Calea către fișierul .docx în folderul assets
file_path = './assets/machetaPlan.docx'

# Afișează conținutul .docx în aplicația Streamlit
docx_text = load_docx(file_path)
st.text(docx_text)

