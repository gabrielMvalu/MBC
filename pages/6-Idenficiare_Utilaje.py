import streamlit as st
import pandas as pd
import re
# Creează o pagină nouă pe Streamlit
st.header(':blue[Prelucrare XLSX]', divider='rainbow')

# Adaugă un widget de încărcare fișier pentru a permite utilizatorului să încarce un fișier XLSX
uploaded_file = st.file_uploader("Încarcă un fișier XLSX", type=['xlsx'])

def extrage_date_financiar(df_financiar):
    values_col2_and_col12 = []
    for index, row in df_financiar.iterrows():
        value_col2 = row.iloc[1]  # Presupunând că coloana 2 este a doua coloană în DataFrame
        value_col12 = row.iloc[11]  # Presupunând că coloana 12 este a 12-a coloană în DataFrame
        if value_col2 == "Total proiect":
            break
        if value_col2 and value_col12 != 0:
            values_col2_and_col12.append((value_col2, value_col12))
    return values_col2_and_col12

def coreleaza_date_financiar_amortizare_ajustat(date_financiar):
    # Citeste fișierul 'utilaje.xlsx' din folderul 'assets' pentru foaia 'amortizare'
    df_amortizare = pd.read_excel('./assets/utilaje.xlsx', sheet_name='amortizare')
    
    amortizare_data = {}
    for index, row in df_amortizare.iterrows():
        if row.iloc[1]:  # Dacă există un nume pentru utilaj
            nume = ' '.join(re.sub(r'\d+$', '', str(row.iloc[1])).strip().split()).lower()
            cod = ' '.join(str(row.iloc[2]).strip().split()) if row.iloc[2] else ''
            descriere = ' '.join(str(row.iloc[3]).strip().split()) if row.iloc[3] else ''
            amortizare_data[nume] = (cod, descriere)

    rezultate_corelate = []
    for nume, cantitate in date_financiar:
        nume_curat = ' '.join(re.sub(r'\d+$', '', str(nume)).strip().split()).lower()
        if nume_curat in amortizare_data:
            cod, descriere = amortizare_data[nume_curat]
            rezultat = f"{nume}, {cantitate} buc., ce aparține clasei {cod} {descriere}, conform HG 2139/2004"
            rezultate_corelate.append((nume, cantitate, rezultat))
    
    return rezultate_corelate




if uploaded_file is not None:
    try:
        df_financiar = pd.read_excel(uploaded_file, sheet_name='P. FINANCIAR')
        date_financiare = extrage_date_financiar(df_financiar)
        if date_financiare:  # Verifică dacă lista nu este goală
            # Calculăm numărul total de utilaje sumând cantitățile
            numar_total_utilaje = sum(cantitate if pd.notnull(cantitate) else 0 for _, cantitate in date_financiare)

            rezultate_corelate = coreleaza_date_financiar_amortizare_ajustat(date_financiare)
            # Crează un DataFrame pentru a afișa rezultatele corelate
            df_rezultate = pd.DataFrame(rezultate_corelate, columns=['Nume', 'Cantitate', 'Rezultat'])
            st.write(df_rezultate)
            st.write(f"Număr total de utilaje: {numar_total_utilaje}")
        else:
            st.error("Nu s-au găsit date valide în foaia 'P. FINANCIAR' pentru calculul numărului de utilaje.")
    except ValueError:
        st.error('Foaia "P. FINANCIAR" nu există în fișierul încărcat. Te rog să încarci un fișier care conține foaia necesară.')
