import streamlit as st
import requests
import pandas as pd
import json
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


st.header("Plausible Log Viewer Check for 404s")

st.sidebar.markdown('''Created by Alan Richardson

[talotics.com](https://talotics.com) | [@talotics](https://twitter.com/talotics)
    ''')

with st.sidebar.expander("Instructions"):
    st.markdown('''
        Enter a domain being tracked in plausible.io, and the API key for your plausible site.

        API keys can be created and revoked from the [plausible.io settings GUI](https://plausible.io/settings#api-keys)
                
        This tool will then check all the urls and report on the 404s.
        ''')
    
defaultAPICode = ""

st.text_input("Domain for stats", key="url")
st.sidebar.text_input("Plausible API key", type="password", key="apikey", value=defaultAPICode)
limitnumber = st.sidebar.number_input("Number of Rows", min_value=1, value=1000,)
grid_height = st.sidebar.number_input("Grid height", min_value=200, max_value=4000, value=400)
periodRange = st.sidebar.selectbox('Time Period',('12 Months', '6 Months', 'This month', '30 Days', '7 Days', 'Today'))




go = st.button("Get")

url = st.session_state.url

if not go:
    st.stop()

if len(url)==0 or len(url.strip())==0:
    st.write("Please Enter a Domain")
    st.stop()

apikey = st.session_state.apikey
if len(apikey)==0 or len(apikey.strip())==0:
    st.write("Please Enter a Plausible API Key")
    st.stop()
    

# Configure the URL

metrics = "visitors,pageviews,events,bounce_rate,visit_duration"
limit = "&limit=" + str(limitnumber)

periodKey = "&period="
periodVals = {'12 Months':"12mo", '6 Months':"6mo", 'This month':"month", '30 Days':"30d", '7 Days':"7d", 'Today':"day"}
period = periodKey + periodVals[periodRange]     

getUrl= "https://plausible.io/api/v1/stats/breakdown?site_id=" + url + period + "&property=event:page" + limit +"&metrics=" + metrics  

#st.write("GET " + getUrl)

#  Get the data
page = requests.get(getUrl, headers={"Authorization":"Bearer " + apikey})

# if not 200 then write an error message
if page.status_code!=200:
    st.markdown('> *Error processing API call* response code: ' + str(page.status_code))
    st.markdown(page.text)
    st.stop()

jsondata = json.loads(page.text)

#st.write(jsondata)


fields = []

# Generic get the keys
item =jsondata['results'][0]
for key, value in item.items():
    fields.append(key)

st.write(fields)

# Get list of items
items= jsondata['results']



# for each url, check for 404s

the404items = []
for item in items:
    checkUrl = "https://" + url + item["page"]
    response = requests.get(checkUrl)
    if(response.status_code == 404):
        st.write([response.status_code, checkUrl])
        the404items.append(item)
    else:
        st.write(checkUrl)





# Prepare Data Grid
gridData = pd.DataFrame(columns=fields)
for item in the404items:
    dataRow = dict()
    for field in fields:
        value = ""
        dataRow[field]=item[field]
    gridData = gridData.append(dataRow, ignore_index=True)






# Prepare AG Grid
gb = GridOptionsBuilder.from_dataframe(gridData)
gb.configure_pagination(paginationAutoPageSize=False,paginationPageSize=50)

# make copy and paste easier
gb.configure_default_column(editable=True)
gb.configure_grid_options(enableCellTextSelection=True)
gb.configure_grid_options(ensureDomOrder=True)

gridOptions = gb.build()

AgGrid(gridData, 
    height=grid_height, 
    width='100%',
    allow_unsafe_jscode=True, #Set it to True to allow cellRenderer function to be injected
    gridOptions=gridOptions)


# https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv
def convert_df(df):
   return df.to_csv().encode('utf-8')


csv = convert_df(gridData)

st.download_button(
   "Download As CSV",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

