import streamlit as st


import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import advertools as adv
from io import StringIO
from dataclasses import make_dataclass
from datetime import datetime

#with open ("default-project.json", "w") as outputFile:
#    json.dump(auditProjectData, outputFile, indent=4)


st.write(datetime.now())

st.header("Sitemap Keywords")

st.write("created by Alan Richardson [talotics.com](https://talotics.com) | [@talotics](https://twitter.com/talotics)")

with st.expander("Instructions"):
    st.markdown('''
        Sitemap keywords experimental GUi
        ''')

@st.cache()
def getSitemapUrls(aUrl):
    if len(sitemapUrl)!=0 and len(sitemapUrl.strip())!=0:
        sitemapData = adv.sitemap_to_df(sitemapUrl)
        sitemapUrls = sitemapData['loc'].tolist()
        return sitemapUrls
    return []

st.text_input("Sitemap URL", key="sitemap")

st.file_uploader("Local Sitemap Data File", key="datafile")

go = st.button("Import")

sitemapUrl = st.session_state.sitemap

#if not go:
#    st.stop()


# process sitemap
sitemapUrls = getSitemapUrls(sitemapUrl)


# process local sitemap data file

datafile = st.session_state.datafile
if datafile is not None:
    fileio = StringIO(datafile.getvalue().decode("utf-8"))
    file_data = fileio.read()
    st.write(file_data)


# Create data as a data_class

@st.cache
def getDataFrame():

    UrlKeywordData = make_dataclass("UrlKeywords", [("url"), ("keywords")])
    sitemapKeywords = []

    for aUrl in sitemapUrls:
            sitemapKeywords.append(UrlKeywordData(aUrl,""))

    return pd.DataFrame(sitemapKeywords)


# Show data in a grid
gridData = getDataFrame()


@st.cache
def getGridOptions(gridData):
    gb = GridOptionsBuilder.from_dataframe(gridData)
    gb.configure_pagination(paginationAutoPageSize=False,paginationPageSize=50)

    # make copy and paste easier
    gb.configure_default_column(editable=True)
    gb.configure_grid_options(enableCellTextSelection=True)
    gb.configure_grid_options(ensureDomOrder=True)
    gridOptions = gb.build()
    return gridOptions

gridOptions = getGridOptions(gridData)

keyword_grid = AgGrid(gridData, gridOptions=gridOptions)

exportGridData = keyword_grid['data']

# https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv
def convert_df(df):
   return df.to_csv().encode('utf-8')


csv = convert_df(exportGridData)

st.download_button(
   "Download As CSV",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)