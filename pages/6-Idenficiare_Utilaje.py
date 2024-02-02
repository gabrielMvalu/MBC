import streamlit as st
import pandas as pd

# Creează o pagină nouă pe Streamlit
st.header(':blue[Prelucrare XLSX]', divider='rainbow')

# Adaugă un widget de încărcare fișier pentru a permite utilizatorului să încarce un fișier XLSX
uploaded_file = st.file_uploader("Încarcă un fișier XLSX", type=['xlsx'])

# Verifică dacă un fișier a fost încărcat
if uploaded_file is not None:
    # Încearcă să citești foaia 'P.FINANCIAR' din fișierul XLSX
    try:
        # Citeste foaia specifică 'P.FINANCIAR'
        df_financiar = pd.read_excel(uploaded_file, sheet_name='P.FINANCIAR')
        
        # Afișează un mesaj de confirmare și datele din foaia 'P.FINANCIAR'
        st.success('Foaia "P.FINANCIAR" a fost găsită și citită cu succes!')
        st.write(df_financiar.head())  # Afișează primele 5 rânduri din DataFrame
    except ValueError:
        # Afișează un mesaj de eroare dacă foaia 'P.FINANCIAR' nu există în fișierul XLSX
        st.error('Foaia "P.FINANCIAR" nu există în fișierul încărcat. Te rog să încarci un fișier care conține foaia necesară.')
