# Import necessary libraries
import requests
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Retrieve API URL and API Key from Streamlit secrets
API_URL = st.secrets['API_URL']
headers = {"Authorization": "Bearer " + st.secrets["API_KEY"]}

# Define a function to make API requests
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# Set up the Streamlit app
if __name__ == '__main__':
    # Define the page title and layout
    page_title = "Formality Classifier"
    layout = "centered"
    
    # Configure the Streamlit app
    st.set_page_config(page_title=page_title, layout=layout)
    st.title(page_title)
    
    # Display a brief description of the app and prompt for user input
    st.write("Welcome to the Formality Classifier app! This app will determine if the inputted text is formal or informal.")
    input_text = st.text_input("Enter text here:")

    # Once the user inputs some text, send a request to the API and wait for the response
    if input_text != "":
        with st.spinner("Waiting for the prediction..."):
            data = query(input_text)
            while "error" in data:
                time.sleep(4)
                data = query(input_text)
            st.success("Prediction complete!")
        
        # Extract the formal and informal scores from the API response and display the result
        formal_score = data[0][1]['score']
        informal_score = data[0][0]['score']
        if formal_score <= 0.5:
            st.write("The inputted text is informal.")
        else:
            st.write("The inputted text is formal.")
        
        # Create a pandas DataFrame to display the scores in a table
        df = pd.DataFrame({'score': [informal_score, formal_score], 'label': ["Informal", "Formal"]})
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # Create a horizontal bar chart to visualize the scores
        fig = px.bar(df, x='score', y='label', orientation='h', color='score')
        st.write(fig)