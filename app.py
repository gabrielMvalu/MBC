# app.py
import streamlit as st
import psutil

st.set_page_config(layout="wide")



# Obținerea utilizării memoriei
mem = psutil.virtual_memory()
mem_usage = f"RAM: {mem.percent}%"

# Obținerea utilizării CPU
cpu_usage = f"CPU: {psutil.cpu_percent()}%"

# Afișarea metricilor în Streamlit
st.metric(label=":green[Utilizare Memorie]", value=mem_usage)
st.metric(label=":green[Utilizare CPU]", value=cpu_usage)

st.header(':blue[Pagina Principală]', divider='rainbow')
st.write(':violet[Bine ați venit la aplicația pentru completarea - Planului de Afaceri! -]')



user_email = st.text_input('Introduceți adresa de email pentru acces:')
if user_email:
    ADMIN_EMAIL = st.secrets["ADMIN_EMAIL"]
    if user_email == ADMIN_EMAIL:
        if st.button('Buton'):
            st.write('Bine ai venit, Robert!')
    else:
        st.write("Nu ai acces la butonul special.")
else:
    st.write("Vă rugăm să introduceți adresa de email pentru a verifica accesul.")
