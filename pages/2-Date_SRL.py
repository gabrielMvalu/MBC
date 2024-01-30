import streamlit as st
from docx import Document
import re
import pandas as pd

# Inițializarea progresului dacă nu există
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Afișează progress bar-ul în sidebar
st.sidebar.write("Progresul tău:")
st.sidebar.progress(st.session_state.progress)


def extract_data_from_docx(doc):
    full_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    company_pattern = r"FURNIZARE INFORMAŢII\n\n(.*?)\n"
    firma_match = re.search(company_pattern, full_text, re.DOTALL)
    firma = firma_match.group(1) if firma_match else "N/A"
    nr_ordine_match = re.search(r"Număr de ordine în Registrul Comerţului: (\w+/\d+/\d+)", full_text)
    nr_ordine = nr_ordine_match.group(1) if nr_ordine_match else "N/A"
    cui_match = re.search(r"Cod unic de înregistrare: (\d+)", full_text)
    cui = cui_match.group(1) if cui_match else "N/A"
    data_infiintarii_match = re.search(r"atribuit în data de (\d+\.\d+\.\d+)", full_text)
    data_infiintarii = data_infiintarii_match.group(1) if data_infiintarii_match else "N/A"
    address_pattern = re.compile(r"Adresă sediu social: (.*?)(?=\n)")
    address_match = re.search(address_pattern, full_text)
    adresa = address_match.group(1) if address_match else "N/A"
    main_activity_pattern = r"Activitatea principală.*?Domeniul de activitate principal:.*?\n(.*?)(?:\n|;)"
    main_activity_match = re.search(main_activity_pattern, full_text, re.DOTALL)
    main_activity = main_activity_match.group(1).strip() if main_activity_match else "N/A"
    section_pattern = re.compile(r"SEDII SECUNDARE / PUNCTE DE LUCRU(.*?)SEDII SI/SAU ACTIVITATI AUTORIZATE", re.DOTALL)
    section_match = re.search(section_pattern, full_text)
    if section_match:
        section_text = section_match.group(1)
        # Extragerea tuturor adreselor din secțiune
        secondary_address_pattern = re.compile(r"Adresă: (.*?)(?=\n)", re.DOTALL)
        adrese_secundare = re.findall(secondary_address_pattern, section_text)
    else:
        adrese_secundare = ["N/A"]
    
    data = {
        "Denumirea firmei": firma,
        "Numărul de ordine în Registrul Comerțului": nr_ordine,
        "Codul unic de înregistrare (CUI)": cui,
        "Data înființării": data_infiintarii,
        "Adresa sediului social": adresa,
        "Activitate principală": main_activity,
        "Adresa sediul secundar": adrese_secundare
    }

    return data

def extract_detailed_info_from_docx(doc):
    text = [p.text for p in doc.paragraphs]
    asociati = {}
    administratori = set()
    in_asociati_section = False
    in_persoane_imputernicite_section = False

    for i in range(len(text)):
        if "ASOCIAŢI PERSOANE FIZICE" in text[i]:
            in_asociati_section = True
            continue
        elif "REPREZENTANT acţionar/asociat/membru" in text[i]:
            in_asociati_section = False

        if in_asociati_section and "Calitate: " in text[i]:
            nume = text[i - 1].strip()
            j = i + 1
            while "Cota de participare la beneficii şi pierderi: " not in text[j] and j < len(text) - 1:
                j += 1
            if j < len(text):
                cota = text[j].split(":")[1].strip()
                asociati[nume] = cota

        if "Persoane împuternicite (PERSOANE FIZICE)" in text[i]:
            in_persoane_imputernicite_section = True
            continue
        elif "Persoane împuternicite (PERSOANE JURIDICE)" in text[i]:
            in_persoane_imputernicite_section = False

        if in_persoane_imputernicite_section and "Calitate: " in text[i]:
            nume_admin = text[i - 1].strip()
            administratori.add(nume_admin)

    output_asociati = []
    for nume, cota in asociati.items():
        info = f"{nume} – asociat cu cota de participare la beneficii și pierderi {cota}"
        if nume in administratori:
            info += " și administrator"
        output_asociati.append(info)

    nume_administrator = ', '.join(administratori)  # Gestionarea cazului cu mai mulți administratori

    return output_asociati, nume_administrator

def extract_situatie_financiara(doc):
    full_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    
    # Definirea pattern-urilor pentru fiecare an
    patterns = {
        "2020": r"SITUAŢIA FINANCIARĂ PE ANUL 2020.*?(?:Numar|Număr) mediu de salari(?:aţi|ati): (\d+)",
        "2021": r"SITUAŢIA FINANCIARĂ PE ANUL 2021.*?(?:Numar|Număr) mediu de salari(?:aţi|ati): (\d+)",
        "2022": r"SITUAŢIA FINANCIARĂ PE ANUL 2022.*?(?:Numar|Număr) mediu de salari(?:aţi|ati): (\d+)"
    }

    data_angajati = {}

    # Căutarea numărului mediu de angajați pentru fiecare an și adăugarea în dicționar
    for an, pattern in patterns.items():
        match = re.search(pattern, full_text, re.DOTALL)
        nr_angajati = match.group(1) if match else "N/A"
        data_angajati[f"Numar mediu angajati {an}"] = nr_angajati

    return data_angajati


def extract_caen_codes(full_text):
    start_marker = "SEDII SI/SAU ACTIVITATI AUTORIZATE"
    end_marker = "CONCORDAT PREVENTIV"
    caen_section_pattern = re.compile(rf"{start_marker}(.*?){end_marker}", re.DOTALL)
    caen_section_match = re.search(caen_section_pattern, full_text)
    
    if caen_section_match:
        caen_section_text = caen_section_match.group(1)
        caen_code_pattern = re.compile(r"(\d{4}) - (.*?)\n")
        caen_codes = re.findall(caen_code_pattern, caen_section_text)
        return caen_codes
    else:
        return []

# Încărcarea și procesarea documentului în Streamlit
st.header(':blue[Încărcare Document Registrul Comerțului]',divider='rainbow')

uploaded_file = st.file_uploader("Trageți fișierul aici sau faceți clic pentru a încărca un document", type=["docx"])

if uploaded_file is not None:
    doc = Document(uploaded_file)
    general_data = extract_data_from_docx(doc)
    detailed_info, admins = extract_detailed_info_from_docx(doc)
    financial_data = extract_situatie_financiara(doc)
    caen_codes = extract_caen_codes("\n".join([p.text for p in doc.paragraphs]))



    # Afișarea datelor în format JSON
    st.json({
        "Date Generale": general_data,
        "Informații Detaliate": {"Asociați": detailed_info, "Administratori": admins},
        "Situație Financiară": financial_data,
        "Coduri CAEN": caen_codes
    })

    # Afișarea datelor în DataFrame-uri pentru vizualizare
    st.write("Date Generale:")
    st.dataframe(pd.DataFrame([general_data]))

    # Convertirea listei de administratori într-o listă de dicționare
    admins_dict = [{"Administratori": admin} for admin in admins]
    # Crearea DataFrame-ului din lista de dicționare
    admins_df = pd.DataFrame(admins_dict)
    # Afișarea DataFrame-ului în Streamlit
    st.write("Administratori:")
    st.dataframe(admins_df)


    st.write("Situație Financiară:")
    st.dataframe(pd.DataFrame(financial_data, columns=["An", "Nr mediu angajați"]))

    st.write("Coduri CAEN:")
    st.dataframe(pd.DataFrame(caen_codes, columns=["Cod CAEN", "Descriere"]))

    # După extragere, salvează datele în session_state
    st.session_state['date_generale'] = general_data
    st.session_state['date_detaliat'] = {"Asociați": detailed_info, "Administratori": admins}
    st.session_state['situatie_financiara'] = financial_data
    st.session_state['coduri_caen'] = caen_codes


    st.session_state.progress += 25  # Sau orice altă valoare specifică paginii
    st.sidebar.progress(st.session_state.progress)
