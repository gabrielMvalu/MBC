# pages/Plan_faceri.py
import streamlit as st
from docx import Document
from pages.constatator import extrage_informatii_firma, extract_asociati_admini, extract_situatie_angajati, extrage_coduri_caen

st.header(':blue_heart: Completare Document cu Placeholder-uri', divider='rainbow')

uploaded_template = st.file_uploader("Încărcați macheta Planului de afaceri", type=["docx"], key="template")
uploaded_document = st.file_uploader("Încărcați documentul Recom constatator.docx", type=["docx"], key="document")

if uploaded_template is not None and uploaded_document is not None:
    template_doc = Document(uploaded_template)
    constatator_doc = Document(uploaded_document)
    
    informatii_firma = extrage_informatii_firma(constatator_doc)
    asociati_admini = extract_asociati_admini(constatator_doc)
    situatie_angajati = extract_situatie_angajati(constatator_doc)
    coduri_caen = extrage_coduri_caen("\n".join([p.text for p in constatator_doc.paragraphs]))

    adrese_secundare_text = '\n'.join(informatii_firma.get('Adresa sediul secundar', [])) if informatii_firma.get('Adresa sediul secundar', []) else "N/A"

    placeholders = {
        "#SRL": informatii_firma.get('Denumirea firmei', 'N/A'),
        "#CUI": informatii_firma.get('Codul unic de înregistrare (CUI)', 'N/A'),
        "#Nr_inmatriculare": informatii_firma.get('Numărul de ordine în Registrul Comerțului', 'N/A'),
        "#data_infiintare": informatii_firma.get('Data înființării', 'N/A'),
        "#Adresa_pct_lucru": adrese_secundare_text,
    }

    def inlocuieste_in_tabele(tabele, placeholders):
        for tabel in tabele:
            for row in tabel.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            for placeholder, value in placeholders.items():
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, value)
                    # Verifică dacă există tabele încastrate în celulă și aplică funcția recursiv
                    if cell.tables:
                        inlocuieste_in_tabele(cell.tables, placeholders)

    inlocuieste_in_tabele(template_doc.tables, placeholders)

    for paragraph in template_doc.paragraphs:
        for run in paragraph.runs:
            for placeholder, value in placeholders.items():
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, value)

    modified_doc_path = "document_modificat.docx"
    template_doc.save(modified_doc_path)

    with open(modified_doc_path, "rb") as file:
        st.download_button(label="Descarcă Documentul Completat", data=file, file_name="document_modificat.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
