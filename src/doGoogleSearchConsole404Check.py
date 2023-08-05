import streamlit as st
import requests
import pandas as pd

st.header("Google Search Console Check for 404s")

st.sidebar.markdown('''Created by Alan Richardson

[talotics.com](https://talotics.com) | [@talotics](https://twitter.com/talotics)
    ''')

with st.sidebar.expander("Instructions"):
    st.markdown('''
        Export the CSV report from the search console 'links' view.
                                
        This tool will then check all the urls and report on the 404s and other status codes.
        ''')
    

urlFieldName = st.sidebar.text_input("URL Field Name", value="Target page")


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    #read csv
    df1=pd.read_csv(uploaded_file)
else:
    st.warning("you need to upload a csv file.")



go = st.button("Check")

if not go:
    st.stop()


# for each url, check for status

for index, row in df1.iterrows():
    checkUrl = df1.iloc[index][urlFieldName]
    response = requests.get(checkUrl)
    st.write(str(response.status_code) + " - " + checkUrl)




