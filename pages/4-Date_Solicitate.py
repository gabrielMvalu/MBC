import streamlit as st
import pandas as pd

def load_excel(file):
    # Function to load the excel file into the session state
    try:
        # Use the 'date solicitate' sheet name as default
        sheet_name = 'date solicitate'
        
        # Load the data into a pandas dataframe
        df = pd.read_excel(file, sheet_name=sheet_name)
        
        # Create a dictionary from the third column
        data_dict = df.iloc[:, 2].to_dict()
        st.session_state['excel_data'] = data_dict
        st.success('Data loaded successfully!')
    except Exception as e:
        st.error(f'An error occurred: {e}')

# Title of the app
st.header(':blue[Incarcati Excel -Date Solicitate.xlsx- pt extragerea datelor]', divider='rainbow')

# File uploader allows user to add their own excel file
uploaded_file = st.file_uploader("Upload your input Excel file", type=["xlsx"])

# Check if the file has been uploaded and if the 'excel_data' key doesn't exist in session state
if uploaded_file is not None and 'excel_data' not in st.session_state:
    load_excel(uploaded_file)


# If the data is loaded, display the data
if 'excel_data' in st.session_state:
    # Retrieve the data from the session state
    excel_data = st.session_state['excel_data']

    # Display the data as JSON
    st.json(excel_data)
    
    # Display the data in DataFrame for visualization
    st.write("Date Solicitate:")
    
    # Create a DataFrame from the dictionary for display
    df_data = pd.DataFrame(list(excel_data.items()), columns=['Row Index', 'Data'])
    st.dataframe(df_data)

    # After extraction, save the data in session_state
    st.session_state['date_solicitate'] = excel_data  # Correct the typo here
