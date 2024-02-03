# pages/Plan_faceri.py
import streamlit as st
from docx import Document

st.header(':blue:[Completare Document cu Placeholder-uri]', divider='rainbow')

uploaded_template = st.file_uploader("Încărcați documentul cu placeholder-uri", type=["docx"], key="template")

if uploaded_template is not None:
    template_doc = Document(uploaded_template)

    # Prelucrare specială pentru adrese secundare
    if 'date_generale' in st.session_state and 'Adresa sediul secundar' in st.session_state['date_generale']:
        adrese_secundare = st.session_state['date_generale']['Adresa sediul secundar']
        adrese_secundare_text = '\n'.join(adrese_secundare) if adrese_secundare else ""

    # Dicționar pentru înlocuirile simple
    placeholders = {
        "#SRL": st.session_state['date_generale'].get('Denumirea firmei', 'N/A'),
        "#CUI": st.session_state['date_generale'].get('Codul unic de înregistrare (CUI)', 'N/A'),
        "#Nr_inmatriculare": st.session_state['date_generale'].get('Numărul de ordine în Registrul Comerțului', 'N/A'),
        "#data_infiintare": st.session_state['date_generale'].get('Data înființării', 'N/A'),
        "#Adresa_pct_lucru": adrese_secundare_text,
    }

    # Înlocuirile în paragrafe
    for paragraph in template_doc.paragraphs:
        for placeholder, value in placeholders.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, value)

    # Înlocuirile în tabele
    for table in template_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for placeholder, value in placeholders.items():
                        if placeholder in paragraph.text:
                            paragraph.text = paragraph.text.replace(placeholder, value)

                # Logica condiționată pentru #Adresa_sediu în celule
                for paragraph in cell.paragraphs:
                    if "#Adresa_sediu" in paragraph.text:
                        if 'numar_total_utilaje' in st.session_state:
                            adresa_sediu_text = f"Număr total de utilaje din sesiune: {st.session_state['numar_total_utilaje']}"
                        else:
                            adresa_sediu_text = st.session_state['date_generale'].get('Adresa sediului social', 'N/A')
                        paragraph.text = paragraph.text.replace("#Adresa_sediu", adresa_sediu_text)

    # Salvarea documentului modificat
    modified_doc_path = "document_modificat.docx"
    template_doc.save(modified_doc_path)

    # Oferă posibilitatea de a descărca documentul modificat
    with open(modified_doc_path, "rb") as file:
        st.download_button(label="Descarcă Documentul Completat", data=file, file_name="document_modificat.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
