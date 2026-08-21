import streamlit as st
import requests
import datetime

'''
# 🚕 TaxiFare Prediction
'''

st.markdown('''
Fill in the ride details below and we'll predict the fare using our trained model,
served live from our Cloud Run API.
''')

st.markdown('### 📅 When is the ride?')
pickup_date = st.date_input('Pickup date', value=datetime.date.today())
pickup_time = st.time_input('Pickup time', value=datetime.datetime.now().time())
pickup_datetime = f'{pickup_date} {pickup_time}'

st.markdown('### 📍 Where does it start and end?')
col1, col2 = st.columns(2)
with col1:
    st.markdown('**Pickup**')
    pickup_longitude = st.number_input('Pickup longitude', value=-73.950655)
    pickup_latitude = st.number_input('Pickup latitude', value=40.783282)
with col2:
    st.markdown('**Dropoff**')
    dropoff_longitude = st.number_input('Dropoff longitude', value=-73.984365)
    dropoff_latitude = st.number_input('Dropoff latitude', value=40.769802)

st.markdown('### 👥 How many passengers?')
passenger_count = st.number_input('Passenger count', min_value=1, max_value=8, step=1, value=1)

url = 'https://taxifare-147738141294.europe-west1.run.app/predict'


params = dict(
    pickup_datetime=pickup_datetime,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=passenger_count,
)

if st.button('🔮 Predict fare'):
    response = requests.get(url, params=params)
    prediction = response.json()
    fare = prediction['fare']

    st.markdown(f'## 💰 Predicted fare: ${fare:.2f}')
