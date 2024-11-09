import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
dorm = pd.read_csv('datasets/Dorm Buildings.csv').sample(frac=1, random_state=42)
non_dorm = pd.read_csv('datasets/Non-Dorm Buildings.csv').sample(frac=1, random_state=42)
weather = pd.read_csv('datasets/Weather Data.csv').sample(frac=1, random_state=42)

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

# Extract energy consumption columns
dorm_energy_columns = [col for col in dorm.columns if 'Consumption' in col]
non_dorm_energy_columns = [col for col in non_dorm.columns if 'Consumption' in col]

# Calculate total energy consumption
dorm_total_energy = dorm[dorm_energy_columns].sum().sum()
non_dorm_total_energy = non_dorm[non_dorm_energy_columns].sum().sum()

# Extract occupancy columns
dorm_occupancy_columns = [col for col in dorm.columns if 'Occupancy' in col]
non_dorm_occupancy_columns = [col for col in non_dorm.columns if 'Occupancy' in col]

# Calculate average occupancy
dorm_avg_occupancy = dorm[dorm_occupancy_columns].mean().mean()
non_dorm_avg_occupancy = non_dorm[non_dorm_occupancy_columns].mean().mean()

# Data for total energy consumption comparison
energy_data = pd.DataFrame({
    'Building Type': ['Dorms', 'Non-Dorms'],
    'Total Energy Consumption (kBTU)': [dorm_total_energy, non_dorm_total_energy]
})

# Data for average occupancy comparison
occupancy_data = pd.DataFrame({
    'Building Type': ['Dorms', 'Non-Dorms'],
    'Average Occupancy': [dorm_avg_occupancy, non_dorm_avg_occupancy]
})

# Plotly Express bar plot for total energy consumption
fig_energy = px.bar(energy_data, x='Building Type', y='Total Energy Consumption (kBTU)', 
                    title='Total Energy Consumption: Dorms vs Non-Dorms', color='Building Type')
st.plotly_chart(fig_energy)

# Plotly Express bar plot for average occupancy
fig_occupancy = px.bar(occupancy_data, x='Building Type', y='Average Occupancy', 
                       title='Average Occupancy: Dorms vs Non-Dorms', color='Building Type')
st.plotly_chart(fig_occupancy)

# Temporal Trends Analysis
st.header('Temporal Trends Analysis')

# Convert 'Series Name' to datetime
for df in [dorm, non_dorm, weather]:
    df['Series Name'] = pd.to_datetime(df['Series Name'], errors='coerce')

# Resample energy consumption data to monthly for temporal trend analysis
dorm_monthly_energy = dorm.set_index('Series Name')[dorm_energy_columns].resample('ME').sum()
non_dorm_monthly_energy = non_dorm.set_index('Series Name')[non_dorm_energy_columns].resample('ME').sum()

# Plot temporal trends for dorm and non-dorm buildings using Plotly
fig_temporal = go.Figure()
fig_temporal.add_trace(go.Scatter(x=dorm_monthly_energy.index, y=dorm_monthly_energy.sum(axis=1),
                                  mode='lines', name='Dorm Buildings', line=dict(color='blue')))
fig_temporal.add_trace(go.Scatter(x=non_dorm_monthly_energy.index, y=non_dorm_monthly_energy.sum(axis=1),
                                  mode='lines', name='Non-Dorm Buildings', line=dict(color='red')))
fig_temporal.update_layout(title='Monthly Energy Consumption Trends: Dorms vs Non-Dorms',
                           xaxis_title='Date', yaxis_title='Total Energy Consumption (kBTU)')
st.plotly_chart(fig_temporal)

# Weather Influence Analysis
st.header('Weather Influence on Energy Consumption and Occupancy')

# Merge weather data with dorm and non-dorm data for correlation analysis
weather.set_index('Series Name', inplace=True)
dorm_weather_combined = pd.concat([dorm_monthly_energy.sum(axis=1), weather['Ohio State University - NOAA Average Daily Temperature (°F)'].resample('M').mean()], axis=1).dropna()
non_dorm_weather_combined = pd.concat([non_dorm_monthly_energy.sum(axis=1), weather['Ohio State University - NOAA Average Daily Temperature (°F)'].resample('M').mean()], axis=1).dropna()

# Plot correlation between temperature and energy consumption using Plotly
fig_weather = go.Figure()
fig_weather.add_trace(go.Scatter(x=dorm_weather_combined.iloc[:, 1], y=dorm_weather_combined.iloc[:, 0],
                                 mode='markers', name='Dorm Buildings', marker=dict(color='blue', opacity=0.6)))
fig_weather.add_trace(go.Scatter(x=non_dorm_weather_combined.iloc[:, 1], y=non_dorm_weather_combined.iloc[:, 0],
                                 mode='markers', name='Non-Dorm Buildings', marker=dict(color='red', opacity=0.6)))
fig_weather.update_layout(title='Impact of Temperature on Energy Consumption',
                          xaxis_title='Average Temperature (°F)', yaxis_title='Total Energy Consumption (kBTU)')
st.plotly_chart(fig_weather)

# Utility-Specific Analysis
st.header('Utility-Specific Energy Consumption Analysis')

# Select a specific utility for analysis (e.g., electricity)
selected_utility = st.selectbox('Select Utility for Analysis', ['Electricity Consumption', 'Chilled Water Consumption', 'Steam Consumption'])

dorm_utility_columns = [col for col in dorm.columns if selected_utility in col]
non_dorm_utility_columns = [col for col in non_dorm.columns if selected_utility in col]

# Calculate monthly consumption for the selected utility
dorm_utility_monthly = dorm.set_index('Series Name')[dorm_utility_columns].resample('M').sum().sum(axis=1)
non_dorm_utility_monthly = non_dorm.set_index('Series Name')[non_dorm_utility_columns].resample('M').sum().sum(axis=1)

# Plot utility-specific trends using Plotly
fig_utility = go.Figure()
fig_utility.add_trace(go.Scatter(x=dorm_utility_monthly.index, y=dorm_utility_monthly,
                                 mode='lines', name='Dorm Buildings', line=dict(color='blue')))
fig_utility.add_trace(go.Scatter(x=non_dorm_utility_monthly.index, y=non_dorm_utility_monthly,
                                 mode='lines', name='Non-Dorm Buildings', line=dict(color='red')))
fig_utility.update_layout(title=f'Monthly {selected_utility}: Dorms vs Non-Dorms',
                          xaxis_title='Date', yaxis_title=f'{selected_utility} (kBTU)')
st.plotly_chart(fig_utility)
