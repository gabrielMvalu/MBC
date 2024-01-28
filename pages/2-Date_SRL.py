import streamlit as st

import streamlit as st
from docx import Document
import re
import pandas as pd

def extract_data_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    full_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    firma_match = re.search(r"FURNIZARE INFORMAŢII\n\n(.*?)\n", full_text, re.DOTALL)
    firma = firma_match.group(1) if firma_match else "N/A"

    nr_ordine_match = re.search(r"Număr de ordine în Registrul Comerţului: (\w+/\d+/\d+)", full_text)
    nr_ordine = nr_ordine_match.group(1) if nr_ordine_match else "N/A"

    cui_match = re.search(r"Cod unic de înregistrare: (\d+)", full_text)
    cui = cui_match.group(1) if cui_match else "N/A"

    data_infiintarii_match = re.search(r"atribuit în data de (\d+\.\d+\.\d+)", full_text)
    data_infiintarii = data_infiintarii_match.group(1) if data_infiintarii_match else "N/A"

    adresa_match = re.search(r"Adresă sediu social: (.*?)(?=\n)", full_text)
    adresa = adresa_match.group(1) if adresa_match else "N/A"

    main_activity_match = re.search(r"Activitatea principală.*?Domeniul de activitate principal:.*?\n(.*?)(?:\n|;)", full_text, re.DOTALL)
    main_activity = main_activity_match.group(1).strip() if main_activity_match else "N/A"

    data = {
        "Denumirea firmei": firma,
        "Numărul de ordine în Registrul Comerțului": nr_ordine,
        "Codul unic de înregistrare (CUI)": cui,
        "Data înființării": data_infiintarii,
        "Adresa sediului social": adresa,
        "Activitate principală": main_activity
    }

    return data

st.title('Încărcare Document Registrul Comertului')

uploaded_file = st.file_uploader("Trageți fișierul aici sau faceți clic pentru a încărca un document", type=["docx"])

if uploaded_file is not None:
    extracted_data = extract_data_from_docx(uploaded_file)
    st.write("Datele extrase din Constatator:")
    st.json(extracted_data)
