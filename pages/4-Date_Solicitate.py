# pages/Date_solicitate.py

import streamlit as st
import pandas as pd

def extract_date_solicitate(df):
    activitate = df.iloc[7, 3]
    CAEN = df.iloc[8, 3]
    nr_locuri_munca_noi = df.iloc[9, 3]
    Judet = df.iloc[10, 3]
    utilaj_dizabilitati = df.iloc[11, 3]
    utilaj_cu_tocator = df.iloc[12, 3]
    adresa_loc_implementare = df.iloc[13, 3]
    nr_clasare_notificare = df.iloc[14, 3]
    clienti_actuali = df.iloc[15, 3]
    furnizori = df.iloc[16, 3]
    tip_activitate = df.iloc[17, 3]
    ISO = df.iloc[18, 3]
    activitate_curenta = df.iloc[19, 3]
    dotari_activitate_curenta = df.iloc[20, 3]
    info_ctr_implementare = df.iloc[21, 3]
    zonele_vizate_prioritar = df.iloc[22, 3]
    utilaj_ghidare = df.iloc[23, 3]
    legaturi = df.iloc[24, 3]
    rude = df.iloc[25, 3]
    concluzie_CA = df.iloc[26, 3]
    caracteristici_tehnice = df.iloc[27, 3]
    flux_tehnologic = df.iloc[28, 3]
    utilajeDNSH = df.iloc[29, 3]

    data = {
        "Activitate": activitate,
        "Cod CAEN": CAEN,
        "Număr locuri de muncă noi": nr_locuri_munca_noi,
        "Județ": Judet,
        "Utilaj pentru persoane cu dizabilități": utilaj_dizabilitati,
        "Utilaj cu tocător": utilaj_cu_tocator,
        "Adresa locației de implementare": adresa_loc_implementare,
        "Număr clasare notificare": nr_clasare_notificare,
        "Clienți actuali": clienti_actuali,
        "Furnizori": furnizori,
        "Tip activitate": tip_activitate,
        "Certificări ISO": ISO,
        "Activitate curentă": activitate_curenta,
        "Dotări pentru activitatea curentă": dotari_activitate_curenta,
        "Informații despre contractul de implementare": info_ctr_implementare,
        "Zonele vizate prioritare": zonele_vizate_prioritar,
        "Utilaj de ghidare": utilaj_ghidare,
        "Legături": legaturi,
        "Rude în cadrul firmei": rude,
        "Concluzii analiza CA": concluzie_CA,
        "Caracteristici tehnice relevante": caracteristici_tehnice,
        "Flux tehnologic": flux_tehnologic,
        "Utilaje DNSH": utilajeDNSH
    }

    return data

st.header('Încărcare Date Solicitate')

uploaded_file = st.file_uploader("Trageți fișierul aici sau faceți clic pentru a încărca", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    solicitate_data = extract_date_solicitate(df)

    st.json({"Date Solicitate": solicitate_data})
    
    st.write("Vizualizare Date Solicitate:")
    st.dataframe(pd.DataFrame([solicitate_data]))

    st.session_state['date_solicitate'] = solicitate_data



