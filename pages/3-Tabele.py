import streamlit as st
import pandas as pd
from pandas import isna
import io
from docx import Document

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
            nr_crt.append(int(counter))  # Asigurăm că 'counter' este întreg, deși este deja de acest tip
            um_list.append("buc")
            
            # Convertim valoarea la întreg înainte de a o adăuga în listă
            # Folosim int() pentru a converti și gestionăm cazurile în care valoarea nu poate fi convertită la int
            try:
                cantitate = int(row[11])
            except ValueError:
                cantitate = None  # Sau o altă valoare de fallback, dacă este necesar
            cantitate_list.append(cantitate)
            
            pret_unitar_list.append(row[3])
            valoare_totala_list.append(row[3] * cantitate if cantitate is not None else None)
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


def df_to_word(document, df, index=False):
    table = document.add_table(rows=(df.shape[0] + 1), cols=df.shape[1])

    # Adăugarea antetului tabelului
    for j in range(df.shape[1]):  # Folosim shape[1] pentru a fi consistenți
        table.cell(0, j).text = df.columns[j]

    # Adăugarea rândurilor din DataFrame în tabel
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):  # Din nou, folosim shape[1] pentru consistență
            val = df.iloc[i, j]  # Folosim iloc pentru a accesa valoarea
            # Verificăm dacă valoarea este NaN sau None și înlocuim cu un șir gol
            text = "" if pd.isna(val) else str(val)
            table.cell(i + 1, j).text = text

    return document


if st.button("Generează Tabel 1"):
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name="P. FINANCIAR")
            tabel_1 = transforma_date(df)

            # Adăugarea DataFrame-ului în documentul Word
            doc = df_to_word(doc, tabel_1)

            # Salvarea documentului într-un obiect BytesIO
            towrite = io.BytesIO()
            doc.save(towrite)
            towrite.seek(0)  # Mergem la începutul stream-ului

            # Crearea unui buton de descărcare pentru documentul Word
            st.download_button(label="Descarcă Tabelul 1 ca Word",
                               data=towrite,
                               file_name="tabel_prelucrat.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        except ValueError as e:
            st.error(f"Eroare la procesarea datelor: {e}")
    else:
        st.error("Te rog să încarci un fișier.")
