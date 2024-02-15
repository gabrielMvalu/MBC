import streamlit as st
import pandas as pd
import spacy
from fuzzywuzzy import process

# Încărcarea modelului spaCy pentru limba română
nlp = spacy.load("ro_core_news_sm")

# Lista de cuvinte cheie pentru utilaje (simplificată pentru exemplu, în limba română)
equipment_keywords = [
    "autogreder", "autogreder cu sistem 3d", "autogudronator", "automacara",
    "automaturatoare cu apa", "autopompa cu malaxor", "autopompa de beton",
    "buldoexcavator", "buldoexcavator cu roti egale", "buldoexcavator cu roti inegale",
    "buldozer", "cilindru compactor terasament", "ciur mobil rotativ", "compactor de sol",
    "compactor/cilindru vibrator compactor", "concasor cu falci si presortare",
    "excavator pe pneuri", "excavator pe senile", "finisor beton", "finisor de asfalt pe pneuri",
    "finisor de asfalt pe senile", "finisorul de asfalt", "foreza", "freza", "freza de asfalt",
    "greder", "incarcator frontal", "incarcator multifunctional cu brat telescopic",
    "incarcator pe pneuri", "macara mobila cu brat telescopic",
    "manipulator telescopic/incarcator multifunctional rotativ", "masina badijonat",
    "masina de colmatat rosturi", "midiexcavatorele", "minibuldoexcavator", "miniexcavator",
    "miniincarcator", "motostivuitor", "panouri fotovoltaice mobile", "pompa de beton",
    "reciclator pentru beton/asfalt", "repartizator mixturi asfaltice", "sistem de ghidare automata",
    "stabilizator terasament", "statia de betoane", "statie de asfalt", "statie mobila de concasare",
    "statie mobila de sortare cu spalare", "telehandler", "tocatorul pentru resturi vegetale",
    "vibroprese fabricare pavele, boltari, borduri", "macara", "masina de repartizat emulsie (autogudronator)",
    "grupul electrogen", "microexcavator", "miniexcavator"
]

def extract_equipment_names(text, equipment_keywords, threshold):
    equipment_found = set()

    # Separarea elementelor pe baza virgulei
    elements = [element.strip().lower() for element in text.split(',')]

    for element in elements:
        # Folosim fuzzy matching pentru a găsi cea mai apropiată potrivire pentru fiecare element
        match, score = process.extractOne(element, equipment_keywords)
        if score >= threshold:
            equipment_found.add(match)

    return equipment_found

# Crearea interfeței Streamlit
st.title('Identificator de Utilaje')

# Slider pentru setarea threshold-ului
threshold = st.slider('Selectați valoarea threshold-ului pentru identificarea utilajelor:', min_value=0, max_value=100, value=80)

# Câmp pentru introducerea textului, cu instrucțiuni pentru utilizator
user_input = st.text_area("Introduceți utilajele separate prin virgulă:")

# Buton pentru procesare
if st.button('Identifică utilaje'):
    # Aplicarea funcției de extragere cu toți parametrii necesari, inclusiv threshold-ul setat de utilizator
    equipment_names = extract_equipment_names(user_input, equipment_keywords, threshold)
    
    # Crearea unui DataFrame pentru afișare
    if equipment_names:
        df = pd.DataFrame(list(equipment_names), columns=['Utilaje Identificate'])
        st.write(df)
    else:
        st.write("Nu au fost identificate utilaje în textul introdus.")
