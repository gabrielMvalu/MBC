# pages/Completare_Doc.py
import streamlit as st
import pandas as pd
from docx import Document
from pages.constatator import extrage_informatii_firma, extrage_asociati_admini, extrage_situatie_angajati, extrage_coduri_caen
from pages.datesolicitate import extrage_date_solicitate
from pages.bilantsianaliza import extrage_date_bilant, extrage_date_contpp, extrage_indicatori_financiari
from pages.ssiutilaje import extrage_pozitii, coreleaza_date

st.set_page_config(layout="wide")

st.header('Procesul de înlocuire a Placeholder-urilor', divider='rainbow')

col1, col2 = st.columns(2)

with col1:
    uploaded_template = st.file_uploader("Încărcați fișierul XLSX Date Solicitate", type=["xlsx"], key="dateSolicitate")

    document_succes = False  # variabilă pentru a ține evidența succesului procesării primului document

    if uploaded_template is not None:
        datesolicitate_doc = pd.read_excel(uploaded_template)
        date_din_xlsx_date_solicitate = extrage_date_solicitate(datesolicitate_doc)

        CAEN_extras = date_din_xlsx_date_solicitate.get('Cod CAEN', 'Cod CAEN necunoscut')
        firma = date_din_xlsx_date_solicitate.get('Denumirea firmei SRL', 'Firmă necunoscută')

        st.success(f"Vom începe prelucrarea firmei: {firma} cu prelucrarea pe codul CAEN: {CAEN_extras}")

        document_succes = True  # Setăm variabila pe True pentru a indica că primul document a fost procesat cu succes

# Utilizarea celei de-a doua coloane pentru încărcarea celui de-al doilea document, dacă primul a fost procesat cu succes
with col2:
    if document_succes:
        uploaded_file2 = st.file_uploader("Încărcați al doilea document", type=["pdf", "docx", "txt"], key="document2")
        # Aici poți adăuga codul pentru procesarea celui de-al doilea document, după ce acesta este încărcat
