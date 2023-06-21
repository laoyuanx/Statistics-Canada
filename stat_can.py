import pandas as pd
import streamlit as st
from stats_can import StatsCan
sc = StatsCan()

#load consumer price index table to df
df = sc.table_to_df("18-10-0004-01")
st.title('Consumner Price Index - Canada')
#st.dataframe(df)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

products_selected = st.multiselect("Pick some keywords:",set(df['Products and product groups']),['All-items','Food','Meat'])
products_to_show = df.loc[products_selected]

# Display the table on the page.
st.dataframe(products_to_show)

chart_data=(df
 #.pivot(index=['GEO','Products and product groups'], columns='REF_DATE', values='VALUE')
 .rename(columns = {"Products and product groups":"ITEM"})
 .query("ITEM in @products_selected and GEO == 'Canada' and REF_DATE >= '2022-01-01'")
 .pivot(index=['REF_DATE'], columns='ITEM', values='VALUE')
 .reset_index()
 .set_index('REF_DATE')
 #.plot()
)

st.line_chart(chart_data)
st.stop()

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('Add a keyword')
  if not fruit_choice:
    streamlit.error("Please provide a keyword")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()
