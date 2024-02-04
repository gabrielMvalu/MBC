import streamlit as st
import pandas as pd
import re

def extrage_pozitii(df_financiar):
    values_col2_and_col12 = []
    for index, row in df_financiar.iterrows():
        value_col2 = row.iloc[1]
        value_col12 = row.iloc[11]
        if value_col2 == "Total proiect":
            break
        if value_col2 and value_col12 and value_col12 != 0:
            values_col2_and_col12.append((value_col2, value_col12))
    return values_col2_and_col12

def coreleaza_date(date_financiar):
    df_amortizare = pd.read_excel('./assets/utilaje.xlsx', sheet_name='amortizare')
    df_utilaje = pd.read_excel('./assets/utilaje1.xlsx', sheet_name='utilajeservicii')
    df_descriere = pd.read_excel(f'./assets/{st.session_state.codCAEN}.xlsx', sheet_name='utilajedescriere')
    
    amortizare_data = {}
    servicii_data = {}
    descriere_data = {}

    for index, row in df_amortizare.iterrows():
        if row.iloc[1]:
            nume = ' '.join(re.sub(r'\d+$', '', str(row.iloc[1])).strip().split()).lower()
            cod = ' '.join(str(row.iloc[2]).strip().split()) if row.iloc[2] else ''
            descriere = ' '.join(str(row.iloc[3]).strip().split()) if row.iloc[3] else ''
            amortizare_data[nume] = (cod, descriere)

    for index, row in df_utilaje.iterrows():
        if row.iloc[1]:
            nume = ' '.join(re.sub(r'\d+$', '', str(row.iloc[1])).strip().split()).lower()
            servicii_data[nume] = nume

    for index, row in df_descriere.iterrows():
        if row.iloc[1]:
            nume = ' '.join(re.sub(r'\d+$', '', str(row.iloc[1])).strip().split()).lower()
            descriere = ' '.join(str(row.iloc[2]).strip().split()) if row.iloc[2] else ''
            descriere_data[nume] = descriere

    rezultate_corelate = []
    rezultate_corelate1 = []
    rezultate_corelate2 = []

    for nume, cantitate in date_financiar:
        nume_curat = ' '.join(re.sub(r'\d+$', '', str(nume)).strip().split()).lower()
        if nume_curat in amortizare_data:
            cod, descriere = amortizare_data[nume_curat]
            rezultat = f"{nume}, {cantitate} buc., ce aparține clasei {cod} {descriere}, conform HG 2139/2004"
            rezultate_corelate.append((nume, cantitate, rezultat))
        if nume_curat in servicii_data:
            rezultat1 = f"{nume}, {cantitate} buc"
            rezultate_corelate1.append((nume, cantitate, rezultat1))
        if nume_curat in descriere_data:
            descriere = descriere_data[nume_curat]
            rezultat2 = f"{nume} - {descriere}"
            rezultate_corelate2.append((nume, cantitate, rezultat2))

    return rezultate_corelate, rezultate_corelate1, rezultate_corelate2


# Oferă utilizatorului opțiunea de a alege un cod CAEN
caen_options = {
    "CAEN 4312": "Lucrări de pregătire a terenului",
    "CAEN 4211": "Lucrări de construcții a drumurilor și autostrăzilor",
    "CAEN 4399": "Alte lucrări speciale de construcții n.c.a.",
    "CAEN 3832": "Recuperarea materialelor reciclabile sortate"
}

st.write("Selectează codul CAEN pentru activitatea ta:")
for caen_code, description in caen_options.items():
    if st.checkbox(f"{caen_code} - {description}"):
        st.session_state.codCAEN = caen_code.split()[1]  # Extrage numărul codului CAEN

# Încărcarea fișierului și procesarea datelor
uploaded_file = st.file_uploader("Încarcă un fișier XLSX", type=['xlsx'])

if uploaded_file is not None and 'codCAEN' in st.session_state:
    try:
        df_financiar = pd.read_excel(uploaded_file, sheet_name='P. FINANCIAR')
        date_financiare = extrage_pozitii(df_financiar)
        if date_financiare:
            rezultate_corelate, rezultate_corelate1, rezultate_corelate2 = coreleaza_date(date_financiare)
            df_rezultate = pd.DataFrame(rezultate_corelate, columns=['Nume', 'Cantitate', 'Rezultat'])
            df_rezultate1 = pd.DataFrame(rezultate_corelate1, columns=['Nume', 'Cantitate', 'Rezultat'])
            df_rezultate2 = pd.DataFrame(rezultate_corelate2, columns=['Nume', 'Cantitate', 'Descriere'])

            # Afișarea rezultatelor
            st.write(df_rezultate)
            st.write(df_rezultate1)
            st.write(df_rezultate2)

            cantitati_corelate = [pd.to_numeric(item[1], errors='coerce') for item in rezultate_corelate]
            cantitati_corelate = [0 if pd.isna(x) else x for x in cantitati_corelate]
            numar_total_utilaje = sum(cantitati_corelate)
            st.write(f"Număr total de utilaje corelate: {numar_total_utilaje}")
      
        else:
            st.error("Nu s-au găsit date valide în foaia 'P. FINANCIAR' pentru calculul numărului de utilaje.")
    except ValueError as e:
        st.error(f'Eroare: {e}')
else:
    if 'codCAEN' not in st.session_state:
        st.error("Selectează un cod CAEN pentru a continua.")
