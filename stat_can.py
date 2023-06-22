import pandas as pd
import streamlit as st
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from stats_can import StatsCan

sc = StatsCan()

START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Consumer Price Index Forecast - Canada')

#stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
#selected_stock = st.selectbox('Select dataset for prediction', stocks)
#load consumer price index table to df
#@st.cache
df = sc.table_to_df("18-10-0004-01")

# User selects series for prediction
products_selected = st.selectbox("Select series for prediction:",set(df['Products and product groups']))

n_years = st.slider('Years of prediction:', 1, 5)
period = n_years * 12
#data_load_state = st.text('Loading data...')
#data = load_data(selected_stock)
#st.subheader('Raw data')
#st.write(data.tail())

# Transform original df to chart_data
data=(df
 #.pivot(index=['GEO','Products and product groups'], columns='REF_DATE', values='VALUE')
 .rename(columns = {"Products and product groups":"ITEM"})
 .query("ITEM in @products_selected and GEO == 'Canada'")
 #.query("ITEM in @products_selected and GEO == 'Canada' and REF_DATE >= '2022-01-01'")
 #.pivot(index=['REF_DATE'], columns='ITEM', values='VALUE')
 #.reset_index()
 #.set_index('REF_DATE')
 #.plot()
)

#data_load_state.text('Loading data... done!')
# Plot raw data
def plot_raw_data(item):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['REF_DATE'], y=data['VALUE'], name=item))
	#fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data(products_selected)
st.stop()
# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)




#Dispaly a line chart
st.line_chart(chart_data)

# Display the table
st.dataframe(chart_data)

st.stop()

try:
  fruit_choice = streamlit.text_input('Add a keyword')
  if not fruit_choice:
    streamlit.error("Please provide a keyword")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()
