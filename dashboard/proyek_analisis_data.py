import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def by_season(day_df):
    byseason = day_df.groupby(['season'])['cnt'].sum().reset_index()
    season_dict = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
    byseason['season'] = byseason['season'].map(season_dict)
    byseason = byseason.assign(cnt_k=lambda x: x['cnt'] / 1000)
    return byseason

def by_registered(day_df):
    byregistered = day_df.groupby(['dteday'])[['casual','registered']].sum().reset_index()
    byregistered['year'] = byregistered['dteday'].dt.year
    byregistered['month'] = byregistered['dteday'].dt.month
    monthly_data = byregistered.groupby(['year', 'month']).agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return monthly_data

day_df = pd.read_csv("https://raw.githubusercontent.com/nisrina-ris/proyek_analisis_data/main/data/day.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

by_season_df = by_season(day_df)

# Calculate monthly_data_2011 and monthly_data_2012
monthly_data_2011 = by_registered(day_df[day_df['dteday'].dt.year == 2011])
monthly_data_2012 = by_registered(day_df[day_df['dteday'].dt.year == 2012])

st.header('Data Analysis: Bike Sharing')

st.subheader('Best Bikes Rental Season')

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt_k", y="season", data=by_season_df.sort_values(by='cnt', ascending=False), hue='season', palette=colors, legend=False)
plt.ylabel(None)
plt.xlabel(None)
plt.title("Number of Rented Bikes by Season", loc="center", fontsize=15)
plt.tick_params(axis ='y', labelsize=12)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.0f}k'.format(x)))

st.pyplot(fig)

st.subheader('Membership by Months for 2011 and 2012')

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)

plt.plot(monthly_data_2011['month'], monthly_data_2011['casual'], marker='o', label='Casual (2011)', color='blue')
plt.plot(monthly_data_2012['month'], monthly_data_2012['casual'], marker='o', label='Casual (2012)', color='orange')
plt.xlabel('Month')
plt.ylabel(None)
plt.title('Casual Bike Rentals Over Months')
plt.legend()
plt.grid(True)
plt.xticks(range(1, 13))

st.pyplot(fig)

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)

plt.plot(monthly_data_2011['month'], monthly_data_2011['registered'], marker='o', label='Registered (2011)', color='green')
plt.plot(monthly_data_2012['month'], monthly_data_2012['registered'], marker='o', label='Registered (2012)', color='red')
plt.xlabel('Month')
plt.ylabel(None)
plt.title('Registered Bike Rentals Over Months')
plt.legend()
plt.grid(True)
plt.xticks(range(1, 13))

st.pyplot(fig)

st.caption('Copyright (c) Dicoding Submission 2024')