import streamlit as st

def show_page():
    st.title("Plan de Afaceri")
    st.write("Descărcați macheta planului de afaceri și completați-o cu informațiile necesare.")

    # Calea către fișierul din folderul assets
    file_path = './assets/machetaPlan.docx'

    # Servește fișierul pentru descărcare
    with open(file_path, "rb") as file:
        btn = st.download_button(
            label="Descărcați Macheta Plan de Afaceri",
            data=file,
            file_name="MachetaPlan.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    # Opțiune pentru încărcarea planului de afaceri completat
    uploaded_file = st.file_uploader("Încărcați planul de afaceri completat:", type=["docx"])
    if uploaded_file is not None:
        st.success("Fișier încărcat cu succes!")
        # Aici poți adăuga logica pentru procesarea documentului încărcat
