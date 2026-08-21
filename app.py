import streamlit as st
import requests
import datetime
import folium
from streamlit_folium import st_folium

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

st.markdown('### 📍 Click the map to set pickup and dropoff points')
st.caption('Select "Pickup" or "Dropoff" below, then click anywhere on the map to place that point.')

if 'pickup' not in st.session_state:
    st.session_state.pickup = (40.783282, -73.950655)
if 'dropoff' not in st.session_state:
    st.session_state.dropoff = (40.769802, -73.984365)

point_to_set = st.radio('Clicking the map sets:', ['Pickup', 'Dropoff'], horizontal=True)

m = folium.Map(location=st.session_state.pickup, zoom_start=12)
folium.Marker(st.session_state.pickup, tooltip='Pickup', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(st.session_state.dropoff, tooltip='Dropoff', icon=folium.Icon(color='red')).add_to(m)

map_data = st_folium(m, width=700, height=500)

if map_data and map_data.get('last_clicked'):
    lat = map_data['last_clicked']['lat']
    lon = map_data['last_clicked']['lng']
    if point_to_set == 'Pickup':
        st.session_state.pickup = (lat, lon)
    else:
        st.session_state.dropoff = (lat, lon)
    st.rerun()

pickup_latitude, pickup_longitude = st.session_state.pickup
dropoff_latitude, dropoff_longitude = st.session_state.dropoff

st.caption(f"📍 Pickup: {pickup_latitude:.5f}, {pickup_longitude:.5f}  |  🎯 Dropoff: {dropoff_latitude:.5f}, {dropoff_longitude:.5f}")

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
