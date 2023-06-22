import pandas as pd
import streamlit as st
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from stats_can import StatsCan

sc = StatsCan()

#START = "2018-01-01"
#TODAY = date.today().strftime("%Y-%m-%d")

st.title('Consumer Price Index Forecast - Canada')

df = sc.table_to_df("18-10-0004-01")

# User selects series for prediction
products_selected = st.selectbox("Select series for prediction:",set(df['Products and product groups']))

n_months = st.slider('Months of prediction:', 1, 3)
period = n_months * 30

# Transform original df to chart_data
data=(df
 #.pivot(index=['GEO','Products and product groups'], columns='REF_DATE', values='VALUE')
 .rename(columns = {"Products and product groups":"ITEM"})
 #.query("ITEM in @products_selected and GEO == 'Canada'")
 .query("ITEM in @products_selected and GEO == 'Canada' and REF_DATE >= '2020-01-01'")
 #.pivot(index=['REF_DATE'], columns='ITEM', values='VALUE')
 #.reset_index()
 #.set_index('REF_DATE')
 #.plot()
)

# Plot raw data
def plot_raw_data(item):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['REF_DATE'], y=data['VALUE'], name='CPI'))
	fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data(products_selected)

# Predict forecast with Prophet.
df_train = data[['REF_DATE','VALUE']]
df_train = df_train.rename(columns={"REF_DATE": "ds", "VALUE": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_months} months')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
