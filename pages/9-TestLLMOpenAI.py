# mbc_docs.py
import streamlit as st
from openai import OpenAI
client = OpenAI()

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
 
   

    st.title('Identificator de Utilaje')
    user_input = st.text_area("Introduceți textul aici:")

    if st.button('Identifică utilaje'):
        # Construirea promptului pentru modelul LLM
        prompt = f"Identifică și listează utilajele menționate în textul: '{user_input}'. Consideră următoarea listă de utilaje: {', '.join(equipment_list)}."

        try:
            # Trimiterea promptului către OpenAI folosind Chat Completions
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "Identifică utilajele din textul următor."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Extragerea și afișarea răspunsului
            st.write("Utilaje identificate:")
            for choice in response.choices:
                st.write(choice.message['content'])
        except Exception as e:
            st.error(f"A apărut o eroare: {e}")
