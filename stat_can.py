import pandas as pd
import streamlit as st
from stats_can import StatsCan
sc = StatsCan()

#load consumer price index table to df
df = sc.table_to_df("18-10-0004-01")
st.title('Consumner Price Index - Canada')
st.dataframe(df)
