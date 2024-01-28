import streamlit as st
import pages.Plan_Afaceri

# Sidebar pentru navigație
st.sidebar.title("Navigație")
page = st.sidebar.selectbox("Alegeți o pagină:", ["Plan de Afaceri"])

# Încărcarea paginilor
if page == "Plan de Afaceri":
    pages.Plan_afaceri.show_page()
