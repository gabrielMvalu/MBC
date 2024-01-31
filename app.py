# app.py
import streamlit as st

ADMIN_EMAIL = st.secrets["ADMIN_EMAIL"]


st.header(':blue[Pagina Principală]', divider='rainbow')
st.write(':violet[Bine ați venit la aplicația pentru completarea - Planului de Afaceri! -]')

# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

# Crează un câmp de input pentru adresa de email
user_email = st.text_input('Introduceți adresa de email pentru acces special:')

# Verifică dacă adresa de email a fost introdusă și corespunde
if user_email:
    if user_email == 'marian@castemill.com':
        # Afișează un buton dacă condiția este îndeplinită
        if st.button('Buton Special pentru Marian'):
            st.write('Bine ai venit, Marian!')
    else:
        st.write("Nu ai acces la butonul special.")
else:
    st.write("Vă rugăm să introduceți adresa de email pentru a verifica accesul special.")
