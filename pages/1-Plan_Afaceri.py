#pages/Plan_faceri.py
import streamlit as st
from docx import Document


# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Pagina 2 - Încărcare și completare document cu placeholder-uri
st.header(':blue[Completare Document cu Placeholder-uri]', divider='rainbow')


# Încărcarea documentului cu placeholder-uri
uploaded_template = st.file_uploader("Încărcați documentul cu placeholder-uri", type=["docx"], key="template")

if uploaded_template is not None:
    template_doc = Document(uploaded_template)

    # Iterează prin fiecare paragraf pentru a căuta și înlocui placeholder-urile
    for paragraph in template_doc.paragraphs:
        for run in paragraph.runs:
            if "#SRL" in run.text:
                run.text = run.text.replace("#SRL", st.session_state['date_generale']['Denumirea firmei'])
            
            if "#CUI" in run.text:
                run.text = run.text.replace("#CUI", st.session_state['date_generale']['Codul unic de înregistrare (CUI)'])
            
            if "#Nr_recom" in run.text:
                run.text = run.text.replace("#Nr_recom", st.session_state['date_generale']['Numărul de ordine în Registrul Comerțului'])
            
   
            # Înlocuirea dată înființare
            if "#Data_infiintare" in run.text:
                run.text = run.text.replace("#Data_infiintare", st.session_state['date_generale']['Data înființării'])
            
            # Condiționarea pentru adresa sediului
            if "#Adresa_sediu" in run.text:
                # Verifică dacă data înființării este egală cu "10.08.2012"
                if st.session_state['date_generale']['Data înființării'] == "10.08.2012":
                    adresa_sediu_text = "tralala"
                else:
                    adresa_sediu_text = f"Adresa sediu: {st.session_state['date_generale']['Adresa sediului social']}\n"
                
                # Înlocuiește placeholder-ul cu adresa de sediu condiționată
                run.text = run.text.replace("#Adresa_sediu", adresa_sediu_text)


            
            if "#Adresa_pct_lucru" in run.text:
                adrese_secundare_formate = '\n'.join(st.session_state['date_generale']['Adresa sediul secundar'])
                adrese_secundare_text = f"Adresa secundara:\n{adrese_secundare_formate}"
                run.text = run.text.replace("#Adresa_pct_lucru", adrese_secundare_text)
                
    # Salvarea documentului modificat
    modified_doc_path = "document_modificat.docx"
    template_doc.save(modified_doc_path)

    # Oferă utilizatorului posibilitatea de a descărca documentul modificat
    with open(modified_doc_path, "rb") as file:
        st.download_button(label="Descarcă Documentul Completat", data=file, file_name="document_modificat.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)

# Verifică dacă progresul este complet
if st.session_state.progress >= 100:
    st.success("Felicitări! Ai completat toate pașii necesari.")
    # Aici poți adăuga orice altă logică necesară pentru a finaliza procesul
    # De exemplu, salvarea datelor, trimiterea unui e-mail de confirmare etc.
else:
    st.error("Atenție: Nu ai completat toate pașii necesari. Te rugăm să te întorci și să finalizezi toate secțiunile.")
    # Oferă utilizatorului opțiuni pentru a reveni la pașii anteriori sau instrucțiuni despre cum să completeze procesul
    # De exemplu, poți oferi linkuri către paginile anterioare sau instrucțiuni specifice
