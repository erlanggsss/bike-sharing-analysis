# dashboard.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page layout
st.set_page_config(page_title="Dashboard Analisis Bike Sharing", layout="wide")

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day_clean.csv")
    hour_df = pd.read_csv("hour_clean.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

# Dashboard title
st.title("Dashboard Analisis Penggunaan Bike Sharing")
st.markdown("Dashboard ini menampilkan tren penggunaan bike sharing berdasarkan dataset yang telah dibersihkan.")

# Sidebar filters
st.sidebar.header("Filter Data")
year_options = ["Semua Tahun"] + list(day_df['year'].unique())
year_filter = st.sidebar.selectbox("Pilih Tahun", year_options)
season_filter = st.sidebar.multiselect("Pilih Musim", day_df['season'].unique(), default=day_df['season'].unique())

# Apply filters
if year_filter != "Semua Tahun":
    filtered_day_df = day_df[(day_df['year'] == year_filter) & (day_df['season'].isin(season_filter))]
    filtered_hour_df = hour_df[(hour_df['year'] == year_filter) & (hour_df['season'].isin(season_filter))]
else:
    filtered_day_df = day_df[day_df['season'].isin(season_filter)]
    filtered_hour_df = hour_df[hour_df['season'].isin(season_filter)]

# Menampilkan Total Sharing Bike, Registered, dan Casual
st.header("Statistik Utama Penggunaan Bike Sharing")

# Menghitung total dari keseluruhan
total_sharing_bike = filtered_day_df['count_cr'].sum()
total_registered = filtered_day_df['registered'].sum()
total_casual = filtered_day_df['casual'].sum()

# Menampilkan total dalam 3 kolom
col1, col2, col3 = st.columns(3)

col1.metric(label="Total Sharing Bike", value=f"{total_sharing_bike:,}")
col2.metric(label="Total Registered", value=f"{total_registered:,}")
col3.metric(label="Total Casual", value=f"{total_casual:,}")

# Divider sebelum visualisasi
st.markdown("---")

# Dashboard sections
st.header("1. Penyewaan Sepeda Berdasarkan Musim")
st.markdown("Grafik ini menunjukkan total penyewaan sepeda pada berbagai musim.")

# Rentals by season chart
seasonal_rentals = filtered_day_df.groupby("season").agg({"count_cr": "sum"}).reset_index()
# Mengatur urutan musim (Spring, Summer, Fall, Winter)
season_order = ["Spring", "Summer", "Fall", "Winter"]
seasonal_rentals['season'] = pd.Categorical(seasonal_rentals['season'], categories=season_order, ordered=True)
seasonal_rentals = seasonal_rentals.sort_values('season')

colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="count_cr", data=seasonal_rentals, palette=colors, ax=ax1)
ax1.set_title("Total Penyewaan Sepeda per Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Penyewaan")
st.pyplot(fig1)

# Divider
st.markdown("---")

# Rentals by hour of the day
st.header("2. Penyewaan Sepeda Berdasarkan Jam")
st.markdown("Bagian ini menunjukkan distribusi penyewaan sepeda sepanjang hari.")

hourly_rentals = filtered_hour_df.groupby("hours").agg({"count_cr": "sum"}).reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x="hours", y="count_cr", data=hourly_rentals, palette="Blues_d", ax=ax2)
ax2.set_title("Penyewaan Sepeda Berdasarkan Jam")
ax2.set_xlabel("Jam (Format 24 Jam)")
ax2.set_ylabel("Total Penyewaan")
st.pyplot(fig2)

# Divider
st.markdown("---")

# Rentals by day of the week
st.header("3. Tren Penggunaan Berdasarkan Hari dalam Seminggu")
st.markdown("Bagian ini menunjukkan penyewaan sepeda berdasarkan hari dalam seminggu.")

weekly_rentals = filtered_hour_df.groupby("one_of_week").agg({"count_cr": "sum"}).reset_index()
# Mengatur urutan hari (Sunday, Monday, ..., Saturday)
day_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
weekly_rentals['one_of_week'] = pd.Categorical(weekly_rentals['one_of_week'], categories=day_order, ordered=True)
weekly_rentals = weekly_rentals.sort_values('one_of_week')

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(x="one_of_week", y="count_cr", data=weekly_rentals, palette=colors, ax=ax3)
ax3.set_title("Penyewaan Sepeda per Hari dalam Seminggu")
ax3.set_xlabel("Hari dalam Seminggu")
ax3.set_ylabel("Total Penyewaan")
st.pyplot(fig3)

# Divider
st.markdown("---")

# Rentals by weather condition
st.header("4. Pengaruh Cuaca terhadap Penyewaan Sepeda")
st.markdown("Bagian ini menjelaskan bagaimana kondisi cuaca memengaruhi jumlah penyewaan sepeda.")

weather_rentals = filtered_hour_df.groupby("weather_situation").agg({"count_cr": "sum"}).reset_index()
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.barplot(x="weather_situation", y="count_cr", data=weather_rentals, palette=colors, ax=ax4)
ax4.set_title("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
ax4.set_xlabel("Kondisi Cuaca")
ax4.set_ylabel("Total Penyewaan")
st.pyplot(fig4)

# Divider
st.markdown("---")

st.markdown("### Terima kasih telah menjelajahi Dashboard Analisis Penggunaan Bike Sharing!")
