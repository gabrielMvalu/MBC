# pages/Date_solicitate.py

import streamlit as st
import pandas as pd

# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

def extract_date_solicitate(df):
    firma = df.iloc[2, 2]
    categ_intreprindere = df.iloc[3, 2]
    firme_legate = df.iloc[4, 2]
    tip_investitie = df.iloc[5, 2]
    activitate = df.iloc[6, 2]
    caen = df.iloc[7, 2]
    nr_locuri_munca_noi = df.iloc[8, 2]
    judet = df.iloc[9, 2]
    utilaj_dizabilitati = df.iloc[10, 2]
    utilaj_cu_tocator = df.iloc[11, 2]
    adresa_loc_implementare = df.iloc[12, 2]
    nr_clasare_notificare = df.iloc[13, 2]
    clienti_actuali = df.iloc[14, 2]
    furnizori = df.iloc[15, 2]
    tip_activitate = df.iloc[16, 2]
    iso = df.iloc[17, 2]
    activitate_curenta = df.iloc[18, 2]
    dotari_activitate_curenta = df.iloc[19, 2]
    info_ctr_implementare = df.iloc[20, 2]
    zonele_vizate_prioritar = df.iloc[21, 2]
    utilaj_ghidare = df.iloc[22, 2]
    legaturi = df.iloc[23, 2]
    rude = df.iloc[24, 2]
    concluzie_CA = df.iloc[36, 2]
    caracteristici_tehnice = df.iloc[37, 2]
    flux_tehnologic = df.iloc[38, 2]
    utilajeDNSH = df.iloc[39, 2]

    data = {
        "Denumirea firmei SRL": firma, 
        "Categorie întreprindere": categ_intreprindere, 
        "Firme legate": firme_legate,  
        "Tipul investiției": tip_investitie,  
        "Activitate": activitate,
        "Cod CAEN": caen,
        "Număr locuri de muncă noi": nr_locuri_munca_noi,
        "Județ": judet,
        "Utilaj pentru persoane cu dizabilități": utilaj_dizabilitati,
        "Utilaj cu tocător": utilaj_cu_tocator,
        "Adresa locației de implementare": adresa_loc_implementare,
        "Număr clasare notificare": nr_clasare_notificare,
        "Clienți actuali": clienti_actuali,
        "Furnizori": furnizori,
        "Tip activitate": tip_activitate,
        "Certificări ISO": iso,
        "Activitate curentă": activitate_curenta,
        "Dotări pentru activitatea curentă": dotari_activitate_curenta,
        "Informații despre contractul de implementare": info_ctr_implementare,
        "Zonele vizate prioritare": zonele_vizate_prioritar,
        "Utilaj de ghidare": utilaj_ghidare,
        "Legături": legaturi,
        "Rude în cadrul firmei": rude,
        "Concluzie_CA": concluzie_CA, 
        "Caracteristici tehnice relevante": caracteristici_tehnice,
        "Flux tehnologic": flux_tehnologic,
        "Utilaje DNSH": utilajeDNSH
    }

    return data

st.header(':blue[Încărcare Date Solicitate]', divider='rainbow')

uploaded_file = st.file_uploader("Trageți fișierul aici sau faceți clic pentru a încărca", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    solicitate_data = extract_date_solicitate(df)

    st.json({"Date Solicitate": solicitate_data})
    
    st.write("Vizualizare Date Solicitate:")
    st.dataframe(pd.DataFrame([solicitate_data]))

    st.toast('Datele sunt retinute pentru procesare', icon='👩🏻‍🏭') 
    
    st.session_state['date_solicitate'] = solicitate_data

    # Actualizează progresul
    st.session_state.progress += 25  
    st.sidebar.progress(st.session_state.progress)
    


