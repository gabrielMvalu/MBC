# pages/Bilant & Analiza.py
import streamlit as st
import pandas as pd

if 'progress' not in st.session_state:
    st.session_state.progress = 0

st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

def extrage_date_bilant(df):
    cpa20 = round(df.iloc[76, 1], 2)
    cpa21 = round(df.iloc[76, 2], 2)
    cpa22 = round(df.iloc[76, 3], 2)

    data = {
        "Capitalul propriu al actionarilor 2020": cpa20, 
        "Capitalul propriu al actionarilor 2021": cpa21,
        "Capitalul propriu al actionarilor 2022": cpa22
    }
    return data

def extrage_date_contpp(df1):
    cpa20 = round(df1.iloc[4, 1], 2)
    cpa21 = round(df1.iloc[4, 2], 2)
    cpa22 = round(df1.iloc[4, 3], 2)
    vt20 = round(df1.iloc[55, 1], 2)
    vt21 = round(df1.iloc[55, 2], 2)
    vt22 = round(df1.iloc[55, 3], 2)
    re20 = round(df1.iloc[66, 1], 2) if df1.iloc[66, 1] > 0 else round(df1.iloc[67, 1], 2)
    re21 = round(df1.iloc[66, 2], 2) if df1.iloc[66, 2] > 0 else round(df1.iloc[67, 2], 2)
    re22 = round(df1.iloc[66, 3], 2) if df1.iloc[66, 3] > 0 else round(df1.iloc[67, 3], 2)
    
    data = {
        "Cifra de afaceri 2020": cpa20, 
        "Cifra de afaceri 2021": cpa21,
        "Cifra de afaceri 2022": cpa22,
        "Venituri totale 2020": vt20, 
        "Venituri totale 2021": vt21,
        "Venituri totale 2022": vt22,
        "Rezultat al exercitiului 2020": re20, 
        "Rezultat al exercitiului 2021": re21,
        "Rezultat al exercitiului 2022": re22,        
    }
    return data


st.header(':blue[Adaugati Analiză, Bilanț, Cont de Profit și Pierdere]', divider='rainbow')

uploaded_file = st.file_uploader("Adăugați fișierul aici sau faceți click pentru a încărca", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, sheet_name='1-Bilant')
    df1 = pd.read_excel(uploaded_file, sheet_name='2-ContPP')
    data_bilant = extrage_date_bilant(df)
    data_contpp = extrage_date_contpp(df1)
    
    st.json({"Datele din bilant sunt:": data_bilant})
    st.json({"Datele din bilant sunt:": data_contpp})    
    
    st.write("Vizualizare Bilant:")
    st.dataframe(pd.DataFrame([data_bilant]))
    st.dataframe(pd.DataFrame([data_contpp]))    
    
    st.session_state['data_bilant'] = data_bilant
    
    st.session_state.progress += 25  
    st.sidebar.progress(st.session_state.progress)

    


