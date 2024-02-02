import streamlit as st
from PIL import Image
import pandas as pd
from io 
from docx import Document
from docx.shared import Pt

st.header(':blue[Pregatirea datelor din P. FINANCIAR pentru completare tabel subcap 2.4]', divider='rainbow')


    # Încărcarea fișierului în sidebar
    uploaded_file = st.sidebar.file_uploader("Încarcă documentul '*.xlsx' aici", type="xlsx", accept_multiple_files=False)
    # Textul care marchează sfârșitul datelor relevante și începutul extracției
    stop_text = "Total proiect"
    # Funcție pentru preluarea și transformarea datelor
    def transforma_date(df):
        stop_index = df.index[df.iloc[:, 1].eq(stop_text)].tolist()
        if stop_index:
            df = df.iloc[3:stop_index[0]]
        else:
            df = df.iloc[3:]
        df = df[df.iloc[:, 1].notna() & (df.iloc[:, 1] != 0) & (df.iloc[:, 1] != '-')]
        df.iloc[:, 6] = df.iloc[:, 6].astype(str)
        # Initialize an empty list for Nr. crt. and the columns that may be skipped
        nr_crt = []
        counter = 1
        um_list = []
        cantitate_list = []
        pret_unitar_list = []
        valoare_totala_list = []
        linie_bugetara_list = []
        # Initialize an empty list for the "Eligibil/ Neeligibil" column
        eligibil_neeligibil = [] 
        for index, row in df.iterrows():
            item = row[1].strip().lower()
            # Check if the cell contains the specific text
            if item in ["total active corporale", "total active necorporale"]:
                nr_crt.append(None)  # Append None for these rows in Nr. crt.
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
                valoare_totala_list.append(row[3]*row[11])
                linie_bugetara_list.append(row[14])
                counter += 1  # Increment the counter only if the condition is not met
        for index, row in df.iterrows():
            # Convert to numeric and handle missing values
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
        # Create the new DataFrame using the list for "Eligibil/ Neeligibil"
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

    # Funcție pentru generarea documentului docx din DataFrame
    def genereaza_docx(df_nou, nume_fisier="Tabel_Prelucrat.docx"):
        # Crearea unui document nou
        document = Document()
        
        # Adăugarea unui titlu
        document.add_heading('Tabel Prelucrat', 0)
    
        # Crearea unui tabel în document
        tabel = document.add_table(rows=1, cols=len(df_nou.columns))
    
        # Popularea rândului de antet
        hdr_cells = tabel.rows[0].cells
        for i, col_name in enumerate(df_nou.columns):
            hdr_cells[i].text = col_name
            hdr_cells[i].paragraphs[0].runs[0].font.bold = True
            hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
    
        # Popularea celulelor tabelului cu date
        for index, row in df_nou.iterrows():
            row_cells = tabel.add_row().cells
            for i, value in enumerate(row):
                row_cells[i].text = str(value)
                row_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
    
        # Salvarea documentului
        docx_io = io.BytesIO()  # Salvarea într-un buffer în memorie pentru a putea fi folosit în Streamlit
        document.save(docx_io)
        docx_io.seek(0)
    
        # Descărcarea documentului în Streamlit
        st.download_button(label="Descarcă Tabelul Prelucrat ca DOCX",
                           data=docx_io,
                           file_name=nume_fisier,
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    
    # Apelarea funcției pentru a genera și descărca documentul, după transformarea datelor
    # df_nou = transforma_date(df)  # Presupunând că df_nou este DataFrame-ul returnat de funcția ta transforma_date
    # genereaza_docx(df_nou)  # Trebuie să apelezi această funcție în codul tău acolo unde este necesar
