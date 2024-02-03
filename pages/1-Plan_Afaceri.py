# pages/Plan_faceri.py
import streamlit as st
from docx import Document
from pages.constatator import extrage_informatii_firma, extract_asociati_admini, extract_situatie_angajati, extrage_coduri_caen

st.header(':blue[Completare Document cu Placeholder-uri]', divider='rainbow')

uploaded_template = st.file_uploader("Încărcați macheta Planului de afaceri", type=["docx"], key="template")

uploaded_document = st.file_uploader("Încărcați documentul  Recom constatator.docx'", type=["docx"], key="document")

if uploaded_template is not None and uploaded_document is not None:
    template_doc = Document(uploaded_template)
    constatator_doc = Document(uploaded_document)
    
    # Extrage informațiile folosind funcțiile din modulul constatator
    informatii_firma = extrage_informatii_firma(constatator_doc)
    asociati_admini = extract_asociati_admini(constatator_doc)
    situatie_angajati = extract_situatie_angajati(constatator_doc)
    coduri_caen = extrage_coduri_caen("\n".join([p.text for p in constatator_doc.paragraphs]))

    # Prelucrare specială pentru adrese secundare
    adrese_secundare_text = '\n'.join(informatii_firma.get('Adresa sediul secundar', [])) if informatii_firma.get('Adresa sediul secundar', []) else "N/A"

    # Dicționar pentru înlocuirile simple în template
    placeholders = {
        "#SRL": informatii_firma.get('Denumirea firmei', 'N/A'),
        "#CUI": informatii_firma.get('Codul unic de înregistrare (CUI)', 'N/A'),
        "#Nr_inmatriculare": informatii_firma.get('Numărul de ordine în Registrul Comerțului', 'N/A'),
        "#data_infiintare": informatii_firma.get('Data înființării', 'N/A'),
        "#Adresa_pct_lucru": adrese_secundare_text,
    }

    # Înlocuirile în paragrafele template-ului
    for paragraph in template_doc.paragraphs:
        for placeholder, value in placeholders.items():
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, value)

    # Înlocuirile în tabelele template-ului
    for table in template_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for placeholder, value in placeholders.items():
                        if placeholder in paragraph.text:
                            paragraph.text = paragraph.text.replace(placeholder, value)

    # Salvarea documentului modificat
    modified_doc_path = "document_modificat.docx"
    template_doc.save(modified_doc_path)

    # Oferă posibilitatea de a descărca documentul modificat
    with open(modified_doc_path, "rb") as file:
        st.download_button(label="Descarcă Documentul Completat", data=file, file_name="document_modificat.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
