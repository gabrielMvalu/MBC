import streamlit as st
import pandas as pd
import io
from docx import Document
from docx.shared import Pt
from io import BytesIO

st.header('Pregătirea datelor din P. FINANCIAR pentru completare tabel subcap 2.4')

uploaded_file = st.file_uploader("Încarcă documentul '*.xlsx' aici", type="xlsx", accept_multiple_files=False)
stop_text = "Total proiect"
def transforma_date(df):
    stop_index = df.index[df.iloc[:, 1].eq(stop_text)].tolist()
    if stop_index:
        df = df.iloc[3:stop_index[0]]
    else:
        df = df.iloc[3:]
    df = df[df.iloc[:, 1].notna() & (df.iloc[:, 1] != 0) & (df.iloc[:, 1] != '-')]
    df.iloc[:, 6] = df.iloc[:, 6].astype(str)
    nr_crt = []
    counter = 1
    um_list = []
    cantitate_list = []
    pret_unitar_list = []
    valoare_totala_list = []
    linie_bugetara_list = []
    eligibil_neeligibil = [] 
    for index, row in df.iterrows():
        item = row[1].strip().lower()
        if item in ["total active corporale", "total active necorporale"]:
            nr_crt.append(None)
            um_list.append(None)
            cantitate_list.append(None)
            pret_unitar_list.append(None)
            valoare_totala_list.append(None)
            linie_bugetara_list.append(None)
        else:
            nr_crt.append(counter)
            um_list.append("buc")
            cantitate_list.append(row[11])
            pret_unitar_list.append(row[3])
            valoare_totala_list.append(row[3] * row[11])
            linie_bugetara_list.append(row[14])
            counter += 1
    for index, row in df.iterrows():
        try:
            val_6 = pd.to_numeric(row[6], errors='coerce')
            val_4 = pd.to_numeric(row[4], errors='coerce')
        except Exception as e:
            st.error(f"Error converting values to numeric: {e}")
            break
        if pd.isna(val_6) or pd.isna(val_4):
            eligibil_neeligibil.append("Data Missing")
        elif val_6 == 0 and val_4 != 0:
            eligibil_neeligibil.append("0 // " + str(round(val_4, 2)))
        elif val_6 == 0 and val_4 == 0:
            eligibil_neeligibil.append("0 // 0")
        elif val_6 < val_4:
            eligibil_neeligibil.append(str(round(val_6, 2)) + " // " + str(round(val_4 - val_6, 2)))
        else:
            eligibil_neeligibil.append(str(round(val_6, 2)) + " // " + str(round(val_6 - val_4, 2)))      
    df_nou = pd.DataFrame({
        "Nr. crt.": nr_crt,
        "Denumirea lucrărilor / bunurilor/ serviciilor": df.iloc[:, 1],
        "UM": um_list,
        "Cantitate": cantitate_list,
        "Preţ unitar (fără TVA)": pret_unitar_list,
        "Valoare Totală (fără TVA)": valoare_totala_list,
        "Linie bugetară": linie_bugetara_list,
        "Eligibil/ neeligibil": eligibil_neeligibil,
        "Contribuie la criteriile de evaluare a,b,c,d": df.iloc[:, 15]
    })
    return df_nou

if st.sidebar.button("Generează Tabel 1"):
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file, sheet_name="P. FINANCIAR")
                tabel_1 = transforma_date(df)
                st.dataframe(tabel_1)  # Afișăm tabelul transformat
                # Conversia DataFrame-ului într-un obiect Excel și crearea unui buton de descărcare
                towrite = BytesIO()
                tabel_1.to_excel(towrite, index=False, engine='openpyxl')
                towrite.seek(0)  # Merem la începutul stream-ului
                st.download_button(label="Descarcă Tabelul 1 ca Excel",
                                   data=towrite,
                                   file_name="tabel_prelucrat.xlsx",
                                   mime="application/vnd.ms-excel")
            except ValueError as e:
               st.error(f"Eroare la procesarea datelor: {e}")
        else:
               st.error("Te rog să încarci un fișier.")
