#pages/Plan_faceri.py
import streamlit as st
from docx import Document

# Pagina 2 - Încărcare și completare document cu placeholder-uri
st.title('Completare Document cu Placeholder-uri')

# Încărcarea documentului cu placeholder-uri
uploaded_template = st.file_uploader("Încărcați documentul cu placeholder-uri", type=["docx"], key="template")

if uploaded_template is not None:
    template_doc = Document(uploaded_template)

    # Iterează prin fiecare paragraf pentru a căuta și înlocui placeholder-urile
    for paragraph in template_doc.paragraphs:
        if "#SRL" in paragraph.text:
            paragraph.text = paragraph.text.replace("#SRL", st.session_state['date_generale']['Denumirea firmei'])
        
        if "#CUI" in paragraph.text:
            paragraph.text = paragraph.text.replace("#CUI", st.session_state['date_generale']['Codul unic de înregistrare (CUI)'])
        
        if "#Nr_recom" in paragraph.text:
            paragraph.text = paragraph.text.replace("#Nr_recom", st.session_state['date_generale']['Numărul de ordine în Registrul Comerțului'])
        
        if "#Data_infiintare" in paragraph.text:
            paragraph.text = paragraph.text.replace("#data_infiintare", st.session_state['date_generale']['Data înființării'])
        
        if "#Adresa_sediu" in paragraph.text:
            paragraph.text = paragraph.text.replace("#Adresa_sediu", st.session_state['date_generale']['Adresa sediului social'])
        
        if "#Adresa_pct_lucru" in paragraph.text:
            adrese_formate = '\n Adresa punct de lucru:'.join(st.session_state['date_generale']['Adresa sediul secundar'])
            paragraph.text = paragraph.text.replace("#Adresa_pct_lucru", adrese_formate)


    # Salvarea documentului modificat
    modified_doc_path = "document_modificat.docx"
    template_doc.save(modified_doc_path)

    # Oferă utilizatorului posibilitatea de a descărca documentul modificat
    with open(modified_doc_path, "rb") as file:
        st.download_button(label="Descarcă Documentul Completat", data=file, file_name="document_modificat.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
