import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

def create_statistic_temperature(df):
    
    return {
        'mean': float("{:.2f}".format(df['TEMP'].mean())), 
        'max': df['TEMP'].max(), 
        'min': df['TEMP'].min()
    }

all_df = pd.read_csv('dataset/all_df.csv')
all_df['full_date'] = pd.to_datetime(all_df['full_date'], format='%Y-%m-%d')
min_date = pd.to_datetime('20130301', format='%Y%m%d')
max_date = pd.to_datetime('20170228', format='%Y%m%d')

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    start_date, end_date = st.date_input(
        label='Date range', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

main_df = all_df[
    (all_df['full_date'] >= pd.to_datetime(start_date)) & (all_df['full_date'] <= pd.to_datetime(end_date))
]

st.header('Dashboard Kondisi Udara')
st.subheader('Summary')

col1, col2, col3 = st.columns(3)
statistic_summary = create_statistic_temperature(main_df)

with col1: 
    st.metric('Average', value=statistic_summary['mean'])

with col2: 
    st.metric('Maximum', value=statistic_summary['max'])

with col3: 
    st.metric('Minimum', value=statistic_summary['min'])

fig, ax = plt.subplots(figsize=(16,8))

group_arr = ['year', 'month'] if ((start_date.year != end_date.year) | (start_date.month != end_date.month)) else ['year', 'month', 'day']

main_df.groupby(by=group_arr).agg({
        'TEMP': ['mean', 'max', 'min']
    }).plot(ax=ax)
plt.title('Grafik Suhu Udara')
plt.xlabel('Tahun dan Bulan')
plt.ylabel('Suhu Udara')
plt.legend(['Suhu Udara Rata-rata', 'Suhu Udara Maximal', 'Suhu Udara Minimal'])
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16,8))
ax = plt.scatter(x=main_df['TEMP'], y=main_df['PRES'], alpha=0.2)
plt.title('Korelasi Suhu dengan Tekanan Udara', fontsize=15)
plt.xlabel('Suhu Udara')
plt.ylabel('Tekanan Udara')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16,8))
ax = plt.scatter(x=main_df['TEMP'], y=main_df['WSPM'], alpha=0.2)
plt.title('Korelasi Suhu dengan Kecepatan Angin', fontsize=15)
plt.xlabel('Suhu Udara')
plt.ylabel('Kecepatan Angin')
st.pyplot(fig)

st.subheader('Kondisi udara')
concentration = ['pm25_ispu', 'pm10_ispu', 'so2_ispu', 'co_ispu', 'o3_ispu', 'no2_ispu']
for i in concentration: 
  fig, ax = plt.subplots(figsize=(16,8))
  parameter = {
      'pm25_ispu': 'PM2.5',
      'pm10_ispu': 'PM10',
      'so2_ispu': 'SO2',
      'co_ispu': 'CO',
      'o3_ispu': 'O3',
      'no2_ispu': 'NO2'
  }
  main_df.groupby(by=['year', 'month', 'day']).agg({
      i: ['mean']
  }).plot(figsize=(20,5), ax=ax)
  plt.title(f'{parameter[i].upper()} ISPU (Index Standar Pencemar Udara) 2015-2016', fontsize=20)
  st.pyplot(fig)




