# pages/Plan_Afaceri.py
# În Plan_Afaceri.py
import streamlit as st
from jinja2 import Environment, FileSystemLoader
from docx import Document

def generate_docx(document_content):
    doc = Document()
    doc.add_paragraph(document_content)
    docx_path = 'plan_de_afaceri_completat.docx'
    doc.save(docx_path)
    return docx_path

if 'date_generale' in st.session_state:
    env = Environment(loader=FileSystemLoader(searchpath='./assets'))
    template = env.get_template('templatejudet.jinja')
    document_generat = template.render(
        date_generale=st.session_state['date_generale'],
        date_detaliat=st.session_state['date_detaliat'],
    )

    # Aici generezi și salvezi documentul .docx
    docx_path = generate_docx(document_generat)

    # Afișează un link de descărcare pentru documentul .docx
    with open(docx_path, "rb") as file:
        btn = st.download_button(
            label="Descarcă Planul de Afaceri",
            data=file,
            file_name="plan_de_afaceri_completat.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

else:
    st.error("Datele necesare nu sunt disponibile. Vă rugăm să procesați un document în pagina 'Date SRL'.")
