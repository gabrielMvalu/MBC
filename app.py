# app.py
import streamlit as st

st.header(':blue[Pagina Principală]', divider='rainbow')
st.write(':violet[Bine ați venit la aplicația pentru completarea - Planului de Afaceri! -]')

# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)


# Verifică dacă există informații despre utilizator
if st.experimental_user:
    user_email = st.experimental_user.email  # Obține adresa de email a utilizatorului
    
    # Verifică dacă adresa de email a utilizatorului corespunde
    if user_email == 'marian@castemill.com':
        # Afișează un buton dacă condiția este îndeplinită
        if st.button('Buton Special pentru Marian'):
            st.write('Bine ai venit, Marian!')
else:
    st.write("Informații despre utilizator nu sunt disponibile.")
