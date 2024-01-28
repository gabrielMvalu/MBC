# pages/Plan_Afaceri.py
import streamlit as st
from jinja2 import Environment, BaseLoader
import os

# Datele de test pentru doi clienți diferiți
date_client_dolj = {
    "firma_nume": "ACDRI LORAMA GRUP S.R.L.",
    "cui": "39324711",
    "judet": "Dolj",
    "nr_utilaje": "5",
    "nr_locuri_munca_noi": "10"
}

date_client_gorj = {
    "firma_nume": "Alta Firma S.R.L.",
    "cui": "12345678",
    "judet": "Gorj",
    "nr_utilaje": "3",
    "nr_locuri_munca_noi": "0"  # Notă: Gorj nu are secțiunea pentru locuri de muncă noi
}

# Selectarea clientului pentru testare
client_selectat = st.radio("Selectează clientul pentru testare:", ("Dolj", "Gorj"))

if client_selectat == "Dolj":
    date_selectate = date_client_dolj
else:
    date_selectate = date_client_gorj

# Determină calea absolută către directorul 'assets'
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, '../assets')

# Crearea și popularea template-ului Jinja2
env = Environment(loader=FileSystemLoader(searchpath=assets_dir))
template = env.get_template('templatejudet.jinja')
document_generat = template.render(**date_selectate)

# Afișarea documentului generat
st.text(document_generat)

