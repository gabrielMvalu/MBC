# pages/Bilant & Analiza.py
import streamlit as st
import pandas as pd

if 'progress' not in st.session_state:
    st.session_state.progress = 0

st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

def extrage_date_bilant(df_bilant):
    cpa20 = df_bilant.iloc[1, 1]
    cpa21 = "{:.2f}".format(df_bilant.iloc[1, 2])
    cpa22 = "{:.2f}".format(df_bilant.iloc[1, 3])

    data_bilant = {
        "Capitalul propriu al actionarilor 2020": cpa20, 
        "Capitalul propriu al actionarilor 2021": cpa21,
        "Capitalul propriu al actionarilor 2022": cpa22
    }
    return data_bilant

def incarca_si_extrage_date(uploaded_file):
    df_bilant = pd.read_excel(uploaded_file, sheet_name='1-Bilant')
    data_bilant = extrage_date_bilant(df_bilant)
    return data_bilant

st.header('Adaugati Analiză, Bilanț, Cont de Profit și Pierdere')

uploaded_file = st.file_uploader("Adăugați fișierul aici sau faceți click pentru a încărca", type=["xlsx"])

if uploaded_file is not None:
    data_bilant = incarca_si_extrage_date(uploaded_file)
    st.session_state['data_bilant'] = data_bilant
    st.session_state.progress += 25  
    st.sidebar.progress(st.session_state.progress)

    
    st.json(data_bilant)
    st.write("Vizualizare Bilant:")
    st.dataframe(pd.DataFrame([data_bilant]))

