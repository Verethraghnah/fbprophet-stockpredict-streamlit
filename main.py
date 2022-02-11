# imports 
import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objects as go 

START = "2015-01-01"
TODAY = date.today().strftime('%Y-%m-%d')

st.title("Streamlit stock prediction app")

# A hardcoded preset of tickers, will add in searchbar for greater flexibility
stocks = ("AAPL", "GOOG", "MSFT", "GME", "AMC", "OCGN")
selected_stock = st.sidebar.selectbox("Select dataset for prediction", stocks)

n_years = st.sidebar.slider("Years of prediction", 1, 4)
period = n_years*365

@st.cache
def load_data(ticker):
    """
    Load data via yahoo finance python API 
    """
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Display message on app to inform user of current state of data
data_load_state = st.sidebar.text("Load data...")
data = load_data(selected_stock)
data_load_state.text("Loading data...done")

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting with Facebook's prophet
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={'Date': 'ds', 'Close': 'y'})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

st.write('forecast graph')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write('forecast components')
fig2 = m.plot_components(forecast)
st.write(fig2)



st.title("Mr. Sonnen's personal forecaster")

crypotocurrencies = ('BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD')
selected_stock = st.selectbox('Select dataset for prediction', crypotocurrencies)

n_years = st.slider('Weeks of prediction:', 1, 4)
period = n_years * 7


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())


# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


plot_raw_data()

# Predict forecast with Prophet.
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet(seasonality_mode='multiplicative')
m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
m.add_country_holidays(country_name='US')
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
fig2 = plot_components_plotly(m, forecast)
st.write(fig2)
