# pages/Plan_Afaceri.py
import streamlit as st
from jinja2 import Environment, FileSystemLoader

# Setează directorul în care se află template-ul
env = Environment(loader=FileSystemLoader(searchpath='./assets'))

# Încarcă template-ul
template = env.get_template('templatejudet.jinja')

# Date de test (le poți înlocui cu datele reale extrase)
date_client = {
    "firma_nume": "Exemplu S.R.L.",
    "cui": "123456789",
    "judet": "Dolj",  # Sau "Gorj" sau altceva, în funcție de client
}

# Generează documentul completat
document_generat = template.render(**date_client)

# Afișează documentul generat în Streamlit
st.text(document_generat)
