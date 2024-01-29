# pages/Plan_Afaceri.py
import streamlit as st
from docx import Document
from docxcompose.composer import Composer
from io import BytesIO

# Funcție pentru procesarea și descărcarea documentului Word
def process_and_download_docx(uploaded_file, data):
    # Încărcați documentul
    doc = Document(uploaded_file)
    composer = Composer(doc)
    
    # Înlocuiți textul folosind datele
    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)

    # Salvați documentul modificat într-un buffer
    buffer = BytesIO()
    composer.save(buffer)
    buffer.seek(0)

    # Returnați buffer-ul pentru descărcare
    return buffer

# Încărcarea documentului Word
uploaded_file = st.file_uploader("Încărcați Planul de Afaceri", type=["docx"])

if uploaded_file is not None and 'date_generale' in st.session_state:
    # Generați buffer-ul pentru documentul modificat
    buffer = process_and_download_docx(uploaded_file, st.session_state['date_generale'])

    # Buton de descărcare pentru documentul modificat
    st.download_button(
        label="Descarcă Planul de Afaceri completat",
        data=buffer,
        file_name="plan_de_afaceri_completat.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.error("Încărcați un document și asigurați-vă că datele necesare sunt disponibile.")
