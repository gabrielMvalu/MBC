# mbc_docs.py
import openai
import streamlit as st

st.set_page_config(layout="wide")

st.header('Pagina Principală')
st.write('Bine ați venit la aplicația pentru completarea Planului de Afaceri!')

# Sidebar pentru cheia API OpenAI
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# Verifică dacă cheia API este introdusă
if not openai_api_key:
    st.info("Vă rugăm să introduceți cheia API OpenAI în bara laterală.")
else:
    # Inițializarea clientului OpenAI cu cheia API introdusă
    openai.api_key = openai_api_key

    # Lista predefinită de utilaje
    equipment_list = [
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
 
   

    # Câmp pentru introducerea textului
    user_input = st.text_area("Introduceți textul aici:")

    # Buton pentru procesare
    if st.button('Identifică utilaje'):
        # Construirea promptului pentru modelul LLM
        prompt = f"Identifică și listează utilajele menționate în textul: '{user_input}'. Consideră următoarea listă de utilaje: {', '.join(equipment_list)}."

        # Trimiterea promptului către OpenAI
        response = openai.Completion.create(
            engine="gpt-4-1106-preview", #  model disponibil
            prompt=prompt,
            temperature=0.3,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Afișarea răspunsului
        st.write("Utilaje identificate:")
        st.write(response.choices[0].text.strip())
