# pages/Date_solicitate.py

import streamlit as st
import pandas as pd

# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

def extract_date_bilant(df):
    firma = df.iloc[2, 2]
    categ_intreprindere = df.iloc[3, 2]
    

    data = {
        "Denumirea firmei SRL": firma, 
        "Categorie întreprindere": categ_intreprindere, 
       
    }

    return data

st.header(':blue[Încărcare 1-Bilant - 2 Cont PP - Analiza financiara]', divider='rainbow')

uploaded_file = st.file_uploader("Trageți fișierul aici sau faceți click pentru a încărca", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    bilant_data = extract_date_bilant(df)

    st.json({"Date Binat & Analiza": bilant_data})
    
    st.write("Vizualizare Bilant & Analiza:")
    st.dataframe(pd.DataFrame([bilant_data]))

    st.session_state['date_bilant'] = bilant_data

    # Actualizează progresul
    st.session_state.progress += 25  
    st.sidebar.progress(st.session_state.progress)
    
