import streamlit as st
import pandas as pd

# Creează o pagină nouă pe Streamlit
st.header(':blue[Prelucrare XLSX]', divider='rainbow')

# Adaugă un widget de încărcare fișier pentru a permite utilizatorului să încarce un fișier XLSX
uploaded_file = st.file_uploader("Încarcă un fișier XLSX", type=['xlsx'])

# Verifică dacă un fișier a fost încărcat
if uploaded_file is not None:
    # Citeste conținutul fișierului XLSX încărcat
    df = pd.read_excel(uploaded_file)

    # Afișează un mesaj de confirmare și primele câteva rânduri din DataFrame pentru a confirma încărcarea cu succes
    st.success('Fișier încărcat cu succes!')
    st.write(df.head())  # Afișează primele 5 rânduri din DataFrame
