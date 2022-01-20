from pickle import FALSE
import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


st.header("Adhoc Web Scraper")

st.write("created by Alan Richardson [talotics.com](https://talotics.com) | [@talotics](https://twitter.com/talotics)")

with st.expander("Instructions"):
    st.markdown('''
        Enter a URL, a CSS Selector and some fields to display.

        e.g. if I want to scrape all links from talotics.com I might use:

        - url:
           - https://talotics.com
        - cssSelector:
           - a
        - attributes:
           - contents,href,target

        This would scrape all the anchor tags and show in a table the contents of the link, the href and the target attribute.

        *NOTE:* _contents_ is not an attribute but will return the _contents_ of an element.

        Useful links about CSS Selectors: [w3schools](https://www.w3schools.com/cssref/css_selectors.asp), [mdn reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors), [CSS Diner Game](https://flukeout.github.io/)
        ''')
st.text_input("Url to scrape", key="url")

# st.text_input("Title", key="title")
st.text_input("Css Selector", key="cssSelector")
st.text_input("csv list of attributes e.g. contents, href, src", key="fields")

go = st.button("Get")

url = st.session_state.url

if not go:
    st.stop()

if len(url)==0 or len(url.strip())==0:
    st.write("Please Enter a URL")
    st.stop()

cssSelector = st.session_state.cssSelector
if len(cssSelector)==0 or len(cssSelector.strip())==0:
    st.write("Please Enter a CSS Selector to Match Items on the Page")
    st.stop()

fields = []
givenFields = st.session_state.fields
if len(givenFields)==0 or len(givenFields.strip())==0:
    fields.append("contents")
else:
    fields = givenFields.replace(" ","").split(",")    

st.write("GET " + url)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
st.write("Select " + cssSelector)
items = soup.select(cssSelector)

gridData = pd.DataFrame(columns=fields)
for item in items:
    dataRow = dict()
    for field in fields:
        value = ""
        try:
            if field=="contents":
                for contentItem in item.contents:
                    value = value + str(contentItem)
                dataRow['contents']=value
            else:
                value = item.get(field,"")

                isList = isinstance(value, list)
                if isList:
                    valueString = ""
                    prepend = ""
                    for valueItem in value:
                        valueString = valueString + prepend + str(valueItem)
                        prepend = ", "
                    value=valueString

                dataRow[field]=value
        except err:
            value = "{ " + field + ", " + str(err) +"}"
            print(value)
            dataRow[field]="err"
    gridData = gridData.append(dataRow, ignore_index=True)



gb = GridOptionsBuilder.from_dataframe(gridData)
gb.configure_pagination(paginationAutoPageSize=False,paginationPageSize=50)

# make copy and paste easier
gb.configure_default_column(editable=True)
gb.configure_grid_options(enableCellTextSelection=True)
gb.configure_grid_options(ensureDomOrder=True)
gridOptions = gb.build()

AgGrid(gridData, gridOptions=gridOptions)


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

with st.expander("Table"):
    st.table(gridData)
