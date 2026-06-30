# app.py

import streamlit as st
import pandas as pd
import paho.mqtt.client as mqtt
import json

st.set_page_config(layout="wide")

if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {}

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    st.session_state.sensor_data = payload

client = mqtt.Client()

client.on_message = on_message

client.connect(
    "broker.hivemq.com",
    1883,
    60
)

client.subscribe("bridge/sensors")

client.loop_start()

st.title("Bridge Monitoring Dashboard")

data = st.session_state.sensor_data

if data:

    cols = st.columns(3)

    sensors = {k:v for k,v in data.items()
               if k != "timestamp"}

    for idx, (name, value) in enumerate(sensors.items()):

        with cols[idx % 3]:
            st.metric(
                label=name,
                value=round(float(value),2)
            )

    df = pd.DataFrame(
        list(sensors.items()),
        columns=["Sensor","Value"]
    )

    st.dataframe(df)

else:
    st.warning("Waiting for sensor data...")
