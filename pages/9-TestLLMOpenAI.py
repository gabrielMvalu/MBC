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
        "tocatorul pentru resturi vegetale",
        # Adaugă restul utilajelor aici
    ]

    # Crearea interfeței Streamlit pentru identificarea utilajelor
    st.title('Identificator de Utilaje')

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
