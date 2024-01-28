# pages/Plan_Afaceri.py
# În Plan_Afaceri.py
import streamlit as st
from jinja2 import Environment, FileSystemLoader

# Verifică dacă datele există în session_state
if 'date_generale' in st.session_state:
    date_client = st.session_state['date_generale']

    # Setează directorul în care se află template-ul
    env = Environment(loader=FileSystemLoader(searchpath='./assets'))

    # Încarcă template-ul
    template = env.get_template('templatejudet.jinja')

    # Generează documentul completat cu datele extrase
    document_generat = template.render(**date_client)

    # Afișează documentul generat în Streamlit
    st.text(document_generat)
else:
    st.write("Nu există date extrase disponibile. Vă rugăm să încărcați și să procesați documentul în pagina Date_SRL.")
