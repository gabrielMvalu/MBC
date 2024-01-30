# pages/Bilant & Analiza.py
import streamlit as st
import pandas as pd

if 'progress' not in st.session_state:
    st.session_state.progress = 0

st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

def extrage_date_bilant(df):
    cpa20 = df.iloc[1, 2]
    cpa21 = df.iloc[78, 1]
    cpa22 = df.iloc[79, 2]

    data_bilant = {
        "Capitalul propriu al actionarilor 2020": cpa20, 
        "Capitalul propriu al actionarilor 2021": cpa21,
        "Capitalul propriu al actionarilor 2022": cpa22
    }
    return data

st.header(':blue[Adaugati Analiză, Bilanț, Cont de Profit și Pierdere]')

uploaded_file = st.file_uploader("Adăugați fișierul aici sau faceți click pentru a încărca", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name='1-Bilant')
    data_bilant = extrage_data_bilant(df)

    st.json({"Datele din bilant sunt:" data_bilant})
    
    st.write("Vizualizare Bilant:")
    st.dataframe(pd.DataFrame([data_bilant]))
    
    st.session_state['data_bilant'] = data_bilant
    st.session_state.progress += 25  
    st.sidebar.progress(st.session_state.progress)

    


