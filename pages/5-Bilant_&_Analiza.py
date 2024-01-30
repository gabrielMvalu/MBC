# pages/Bilant & Analiza.py
import streamlit as st
import pandas as pd

# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

def extrage_date_foaie(df):
    # Presupunem că valorile sunt deja în format float în DataFrame
    valoare1 = Decimal(df.iloc[9, 1]).quantize(Decimal('0.00'))
    valoare2 = Decimal(df.iloc[10, 1]).quantize(Decimal('0.00'))

    data = {
        "Valoare1": valoare1, 
        "Valoare2": valoare2,
    }

    return data

def incarca_si_extrage_date(uploaded_file):
    df_bilant = pd.read_excel(uploaded_file, sheet_name='1-Bilant')
    data_bilant = extrage_date_foaie(df_bilant)

    df_contpp = pd.read_excel(uploaded_file, sheet_name='1-ContPP')
    data_contpp = extrage_date_foaie(df_contpp)

    return data_bilant, data_contpp

st.header('Încărcare și Analiză Bilanț și Cont de Profit și Pierdere')

uploaded_file = st.file_uploader("Adăugați fișierul aici sau faceți click pentru a încărca", type=["xlsx"])

if uploaded_file is not None:
    data_bilant, data_contpp = incarca_si_extrage_date(uploaded_file)

    # Stocarea datelor în st.session_state pentru utilizare ulterioară în aplicație
    st.session_state['data_bilant'] = data_bilant
    st.session_state['data_contpp'] = data_contpp

    # Actualizează progresul
    st.session_state.progress += 25  
    st.sidebar.progress(st.session_state.progress)


   
    st.write("Vizualizare Bilant:")
    st.dataframe(pd.DataFrame([data_bilant]))
    st.write("Vizualizare Analiza:")
    st.dataframe(pd.DataFrame([data_contpp]))
