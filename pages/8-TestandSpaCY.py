import streamlit as st
import pandas as pd
import spacy

# Încărcarea modelului spaCy pentru limba română
nlp = spacy.load("ro_core_news_sm")

# Lista de cuvinte cheie pentru utilaje (simplificată pentru exemplu, în limba română)
equipment_keywords = ["excavator", "buldoexcavator", "motofierăstrău"]

# Funcția pentru extragerea denumirilor de utilaje
def extract_equipment_names(text):
    doc = nlp(text)
    equipment_found = set()
    for token in doc:
        # Adaptarea condiției pentru a se potrivi mai bine cu structura limbii române
        if token.pos_ in ["PROPN", "NOUN"] and any(keyword in token.text.lower() for keyword in equipment_keywords):
            equipment_found.add(token.text)
    return equipment_found

# Crearea interfeței Streamlit
st.title('Identificator de Utilaje în Limba Română')

# Câmp pentru introducerea textului
user_input = st.text_area("Introduceți textul aici:", "Excavator pe șenile, miniexcavator CAT 308CR NOU 2023 - Controlul croazieră pentru selectarea vitezei constante de deplasare.")

# Buton pentru procesare
if st.button('Identifică utilaje'):
    # Aplicarea funcției de extragere
    equipment_names = extract_equipment_names(user_input)
    
    # Crearea unui DataFrame pentru afișare
    if equipment_names:
        df = pd.DataFrame(equipment_names, columns=['Utilaje Identificate'])
        st.write(df)
    else:
        st.write("Nu au fost identificate utilaje în textul introdus.")
