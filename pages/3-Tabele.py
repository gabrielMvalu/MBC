import streamlit as st
import pandas as pd
import io
from docx import Document
from docx.shared import Pt

st.header('Pregătirea datelor din P. FINANCIAR pentru completare tabel subcap 2.4')

uploaded_file = st.sidebar.file_uploader("Încarcă documentul '*.xlsx' aici", type="xlsx", accept_multiple_files=False)

def transforma_date(df):
    stop_text = "Total proiect"
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
            # Conversie în numerice și verificare NaN
            try:
                cantitate = pd.to_numeric(row[11], errors='coerce')
                pret_unitar = pd.to_numeric(row[3], errors='coerce')
                if pd.notna(cantitate) and pd.notna(pret_unitar):
                    valoare_totala = cantitate * pret_unitar
                else:
                    valoare_totala = None  # Sau altă valoare implicită, cum ar fi 0
            except Exception as e:
                valoare_totala = None  # Sau gestionează eroarea după caz
                st.error(f"Eroare la convertirea sau calculul valorilor: {e}")

            cantitate_list.append(cantitate)
            pret_unitar_list.append(pret_unitar)
            valoare_totala_list.append(valoare_totala)
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
            eligibil_neeligibil.append("0 // " + str(round(val_4,2)))
        elif val_6 == 0 and val_4 == 0:
            eligibil_neeligibil.append("0 // 0")
        elif val_6 < val_4:
            eligibil_neeligibil.append(str(round(val_6,2)) + " // " + str(round(val_4 - val_6,2)))
        else:
            eligibil_neeligibil.append(str(round(val_6,2)) + " // " + str(round(val_6 - val_4,2)))      
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

def genereaza_docx(df_nou, nume_fisier="Tabel_Prelucrat.docx"):
    document = Document()
    document.add_heading('Tabel Prelucrat', 0)
    tabel = document.add_table(rows=1, cols=len(df_nou.columns))
    hdr_cells = tabel.rows[0].cells
    for i, col_name in enumerate(df_nou.columns):
        hdr_cells[i].text = col_name
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
    for index, row in df_nou.iterrows():
        row_cells = tabel.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)
            row_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
    docx_io = io.BytesIO()
    document.save(docx_io)
    docx_io.seek(0)
    st.download_button(label="Descarcă Tabelul Prelucrat ca DOCX",
                       data=docx_io,
                       file_name=nume_fisier,
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df_transformed = transforma_date(df)
    genereaza_docx(df_transformed)

