# pages/Plan_faceri.py
import streamlit as st
from docx import Document
from pages.constatator import extrage_informatii_firma, extract_asociati_admini, extract_situatie_angajati, extrage_coduri_caen
from pages.datesolicitate import extrage_date_solicitate

st.set_page_config(layout="wide")
st.header(':blue[Completare Document cu Placeholder-uri]', divider='rainbow')

col1, col2 = st.columns(2)
with col1:
    uploaded_template = st.file_uploader("Încărcați macheta Planului de afaceri", type=["docx"], key="template")
    st.info('Se va adauga doar documente ce urmeaza a fi procesate Plan afacer, Cerere de finantare etc.', icon="ℹ️")

with col2:
    uploaded_document = st.file_uploader("Încărcați documentul Recom constatator.docx", type=["docx"], key="document")
    st.info('Se vor incarca doar documente docx si doar Raportul interogare', icon="ℹ️")

col3, col4 = st.columns(2)
with col3:
    uploaded_file1 = st.file_uploader("Încărcați fișierul aici sau faceți clic pentru a încărca", type=["xlsx"], key="excelSolicitate")
with col4:
    st.write('Text text')

if uploaded_template is not None and uploaded_document is not None and uploaded_file1 is not None:
    template_doc = Document(uploaded_template)
    st.toast('Incepem procesarea Planului de afaceri', icon='⭐')     
    constatator_doc = Document(uploaded_document)
    date_solicitate_doc = Document(uploaded_file1)
     
    informatii_firma = extrage_informatii_firma(constatator_doc)
    asociati_info, administratori_info = extract_asociati_admini(constatator_doc)
    situatie_angajati = extract_situatie_angajati(constatator_doc)
    coduri_caen = extrage_coduri_caen("\n".join([p.text for p in constatator_doc.paragraphs]))
    date_solicitate = extrage_date_solicitate(date_solicitate_doc)
    
    
    def curata_duplicate_coduri_caen(coduri_caen):
        coduri_unice = {}
        for cod, descriere in coduri_caen:
            coduri_unice[cod] = descriere
        return list(coduri_unice.items())

    coduri_caen_curatate = curata_duplicate_coduri_caen(coduri_caen)
    
    adrese_secundare_text = '\n'.join(informatii_firma.get('Adresa sediul secundar', [])) if informatii_firma.get('Adresa sediul secundar', []) else "N/A"
    asociati_text = '\n'.join(asociati_info) if asociati_info else "N/A"
    administratori_text = administratori_info if administratori_info else "N/A"
    coduri_caen_text = '\n'.join([f"{cod} - {descriere}" for cod, descriere in coduri_caen_curatate]) if coduri_caen_curatate else "N/A"    

    placeholders = {
        "#SRL": informatii_firma.get('Denumirea firmei', 'N/A'),
        "#CUI": informatii_firma.get('Codul unic de înregistrare (CUI)', 'N/A'),
        "#Nr_inmatriculare": informatii_firma.get('Numărul de ordine în Registrul Comerțului', 'N/A'),
        "#data_infiintare": informatii_firma.get('Data înființării', 'N/A'),
        "#Adresa_sediu": informatii_firma.get('Adresa sediului social','N/A'),
        "#Adresa_pct_lucru": adrese_secundare_text,
        "#Asociati": asociati_text,
        "#Administrator": administratori_text,
        "#activitatePrincipala": informatii_firma.get('Activitate principală','N/A'),
        "#CAENautorizate": coduri_caen_text,


        "#categorie_intreprindere": date_solicitate.get('Categorie întreprindere', 'N/A'), 
        "#Firme_legate": date_solicitate.get('Firme legate', 'N/A'),  
        "#Tip_investitie": date_solicitate.get('Tipul investiției', 'N/A'),  
        "#activitate": date_solicitate.get('Activitate', 'N/A'),
        "#CAEN": date_solicitate.get('Cod CAEN', 'N/A'),
        "#nr_locuri_munca_noi": date_solicitate.get('Număr locuri de muncă noi', 'N/A'),
        "#Judet": date_solicitate.get('Județ', 'N/A'),
        "#utilaj_dizabilitati": date_solicitate.get('Utilaj pentru persoane cu dizabilități', 'N/A'),
        "#utilaj_cu_tocator": date_solicitate.get('Utilaj cu tocător', 'N/A'),
        "#adresa_loc_implementare": date_solicitate.get('Adresa locației de implementare', 'N/A'),
        "#nr_clasare_notificare": date_solicitate.get('Număr clasare notificare', 'N/A'),
        "#clienti_actuali": date_solicitate.get('Clienți actuali', 'N/A'),
        "#furnizori": date_solicitate.get('Furnizori', 'N/A'),
        "#tip_activitate": date_solicitate.get('Tip activitate', 'N/A'),
        "#ISO": date_solicitate.get('Certificări ISO', 'N/A'),
        "#activitate_curenta": date_solicitate.get('Activitate curentă', 'N/A'),
        "#dotari_activitate_curenta": date_solicitate.get('Dotări pentru activitatea curentă', 'N/A'),
        "#info_ctr_implementare": date_solicitate.get('Informații despre contractul de implementare', 'N/A'),
        "#zonele_vizate_prioritar": date_solicitate.get('Zonele vizate prioritare', 'N/A'),
        "#utilaj_ghidare": date_solicitate.get('Utilaj de ghidare', 'N/A'),
        "legaturi": date_solicitate.get('Legături', 'N/A'),
        "#rude": date_solicitate.get('Rude în cadrul firmei', 'N/A'),
        "#concluzie_CA": date_solicitate.get('Concluzie_CA', 'N/A'), 
        "#caracteristici_tehnice": date_solicitate.get('Caracteristici tehnice relevante', 'N/A'),
        "#flux_tehnologic": date_solicitate.get('Flux tehnologic', 'N/A'),
        "#utilajeDNSH": date_solicitate.get('Utilaje DNSH', 'N/A'),
        "#descriere_utilaj_ghidare": date_solicitate.get('Utilaj ghidare', 'N/A'),      
    }

    def inlocuieste_in_tabele(tabele, placeholders):
        for tabel in tabele:
            for row in tabel.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            for placeholder, value in placeholders.items():
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, value)
                    # Verifică dacă există tabele încastrate în celulă și aplică funcția recursiv
                    if cell.tables:
                        inlocuieste_in_tabele(cell.tables, placeholders)

    inlocuieste_in_tabele(template_doc.tables, placeholders)

    for paragraph in template_doc.paragraphs:
        for run in paragraph.runs:
            for placeholder, value in placeholders.items():
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, value)

    modified_doc_path = "document_modificat.docx"
    template_doc.save(modified_doc_path)

    with open(modified_doc_path, "rb") as file:
        st.download_button(label="Descarcă Documentul Completat", data=file, file_name="document_modificat.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
