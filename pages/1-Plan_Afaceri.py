# pages/Plan_Afaceri.py
# În Plan_Afaceri.py
import streamlit as st
from jinja2 import Environment, FileSystemLoader

# Verifică dacă datele sunt disponibile în session_state
if 'date_generale' in st.session_state:
    env = Environment(loader=FileSystemLoader(searchpath='./assets'))
    template = env.get_template('templatejudet.jinja')
    document_generat = template.render(
        date_generale=st.session_state['date_generale'],
        date_detaliat=st.session_state['date_detaliat'],
        # Include aici și alte date necesare din session_state
    )
    st.text(document_generat)
else:
    st.error("Datele necesare nu sunt disponibile. Vă rugăm să procesați un document în pagina 'Date SRL'.")
