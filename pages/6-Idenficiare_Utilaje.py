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
    amortizare_data = {}
    servicii_data = {}

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

    rezultate_corelate = []
    rezultate_corelate1 = []

    for nume, cantitate in date_financiar:
        nume_curat = ' '.join(re.sub(r'\d+$', '', str(nume)).strip().split()).lower()
        if nume_curat in amortizare_data:
            cod, descriere = amortizare_data[nume_curat]
            rezultat = f"{nume}, {cantitate} buc., ce aparține clasei {cod} {descriere}, conform HG 2139/2004"
            rezultate_corelate.append((nume, cantitate, rezultat))
        if nume_curat in servicii_data:
            rezultat1 = f"{nume}, {cantitate} buc"
            rezultate_corelate1.append((nume, cantitate, rezultat1))

    return rezultate_corelate, rezultate_corelate1

uploaded_file = st.file_uploader("Încarcă un fișier XLSX", type=['xlsx'])

if uploaded_file is not None:
    try:
        df_financiar = pd.read_excel(uploaded_file, sheet_name='P. FINANCIAR')
        date_financiare = extrage_pozitii(df_financiar)
        if date_financiare:
            rezultate_corelate, rezultate_corelate1 = coreleaza_date(date_financiare)
            df_rezultate = pd.DataFrame(rezultate_corelate, columns=['Nume', 'Cantitate', 'Rezultat'])
            df_rezultate1 = pd.DataFrame(rezultate_corelate1, columns=['Nume', 'Cantitate', 'Rezultat'])
            st.write(df_rezultate)
            st.write(df_rezultate1)

            cantitati_corelate = [pd.to_numeric(item[1], errors='coerce') for item in rezultate_corelate]
            cantitati_corelate = [0 if pd.isna(x) else x for x in cantitati_corelate]
            numar_total_utilaje = sum(cantitati_corelate)
            st.write(f"Număr total de utilaje corelate: {numar_total_utilaje}")
      
        else:
            st.error("Nu s-au găsit date valide în foaia 'P. FINANCIAR' pentru calculul numărului de utilaje.")
    except ValueError as e:
        st.error(f'Eroare: {e}')
