# pages/Completare_Doc.py
import streamlit as st
import pandas as pd
from docx import Document
from pages.constatator import extrage_informatii_firma, extrage_asociati_admini, extrage_situatie_angajati, extrage_coduri_caen
from pages.datesolicitate import extrage_date_solicitate
from pages.bilantsianaliza import extrage_date_bilant, extrage_date_contpp, extrage_indicatori_financiari
from pages.ssiutilaje import extrage_pozitii, coreleaza_date

st.set_page_config(layout="wide")

st.header(':blue[Procesul de inlocuire a Placeholder-uri]', divider='rainbow')

uploaded_template = st.file_uploader("Încărcați fisieru XLSX Date Solicitate", type=["xlsx"], key="dateSolicitate")

if uploaded_template is not None:
  datesolicitate_doc = pd.read_excel(uploaded_file1)
  date_din_xlsx_date_solicitate = extrage_date_solicitate(datesolicitate_doc)
  
  # Declararea si initializarea variabilei CAEN_extras cu codul CAEN extras
  CAEN_extras = date_din_xlsx_date_solicitate['Cod CAEN']

  # Afisarea mesajului cu numele firmei și codul CAEN
  st.success(f"Vom începe prelucrarea firmei: {date_din_xlsx_date_solicitate['Denumirea firmei SRL']} cu prelucrarea pe codul CAEN: {date_din_xlsx_date_solicitate['Cod CAEN']}")


