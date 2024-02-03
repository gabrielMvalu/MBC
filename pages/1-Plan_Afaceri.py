# pages/Plan_faceri.py
import streamlit as st
from docx import Document
from pages.constatator import extrage_informatii_firma, extract_asociati_admini, extract_situatie_angajati, extrage_coduri_caen

st.header(':blue[Completare Document cu Placeholder-uri]', divider='rainbow')

uploaded_template = st.file_uploader("Încărcați macheta Planului de afaceri", type=["docx"], key="template")
uploaded_document = st.file_uploader("Încărcați documentul Recom constatator.docx", type=["docx"], key="document")

if uploaded_template is not None and uploaded_document is not None:
    template_doc = Document(uploaded_template)
    st.toast('Incepem procesarea Planului de afaceri', icon='⭐')     
    
    constatator_doc = Document(uploaded_document)
    st.toast('Datele din Recom sunt prelucrate', icon='⭐')     
    
    informatii_firma = extrage_informatii_firma(constatator_doc)
    asociati_info, administratori_info = extract_asociati_admini(constatator_doc)
    situatie_angajati = extract_situatie_angajati(constatator_doc)
    coduri_caen = extrage_coduri_caen("\n".join([p.text for p in constatator_doc.paragraphs]))

    def curata_duplicate_coduri_caen(coduri_caen):
        coduri_unice = {}
        for cod, descriere in coduri_caen:
            coduri_unice[cod] = descriere
        return list(coduri_unice.items())

    coduri_caen_curatate = curata_duplicate_coduri_caen(coduri_caen)
    
    adrese_secundare_text = '- \n'.join(informatii_firma.get('Adresa sediul secundar', [])) if informatii_firma.get('Adresa sediul secundar', []) else "N/A"
    asociati_text = '- \n'.join(asociati_info) if asociati_info else "N/A"
    administratori_text = administratori_info if administratori_info else "N/A"
    coduri_caen_text = '\n'.join([f"{cod} - {descriere}" for cod, descriere in coduri_caen_curatate]) if coduri_caen_curatate else "N/A"    

    placeholders = {
        "#SRL": informatii_firma.get('Denumirea firmei', 'N/A'),
        "#CUI": informatii_firma.get('Codul unic de înregistrare (CUI)', 'N/A'),
        "#Nr_inmatriculare": informatii_firma.get('Numărul de ordine în Registrul Comerțului', 'N/A'),
        "#data_infiintare": informatii_firma.get('Data înființării', 'N/A'),
        "#Adresa_sediu": informatii_firma.get('Adresa sediului social','N/A'),
        "#Adresa_pct_lucru": adrese_secundare_text,
        "#Asociati": asociati_text,
        "#Administrator": administratori_text,
        "#activitatePrincipala": informatii_firma.get('Activitate principală','N/A'),
        "#CAENautorizate": coduri_caen_text,
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
