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


user_email = st.text_input('Introduceți adresa de email pentru acces special:')
if user_email:
   ADMIN_EMAIL = st.secrets["ADMIN_EMAIL"]
    if user_email == ADMIN_EMAIL:
        if st.button('Buton Special pentru Robert'):
            st.write('Bine ai venit, Robert!')
    else:
        st.write("Nu ai acces la butonul special.")
else:
    st.write("Vă rugăm să introduceți adresa de email pentru a verifica accesul special.")
