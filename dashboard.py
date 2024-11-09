import streamlit as st
import pandas as pd
import numpy as np

dorm = pd.read_csv('datasets/Dorm Buildings.csv.')
non_dorm = pd.read_csv('datasets/Non-Dorm Buildings.csv.')
weather = pd.read_csv('datasets/Weather Data.csv.')


st.title('Dorm vs Non-Dorm Buildings Energy Consumption')
st.write('This dashboard compares the energy consumption of dorm and non-dorm buildings at a university.')
st.header('Dataset Overview')

# Display the first few rows of each dataset
st.subheader('Dorm Buildings Data')
st.write(dorm.head())

st.subheader('Non-Dorm Buildings Data')
st.write(non_dorm.head())

st.subheader('Weather Data')
st.write(weather.head())

# Display basic statistics for each dataset
st.subheader('Dorm Buildings Data Statistics')
st.write(dorm.describe())

st.subheader('Non-Dorm Buildings Data Statistics')
st.write(non_dorm.describe())

st.subheader('Weather Data Statistics')
st.write(weather.describe())


# Display the total energy consumption for each building type
st.header('Total Energy Consumption')
