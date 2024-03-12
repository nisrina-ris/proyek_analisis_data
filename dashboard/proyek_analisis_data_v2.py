import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def by_season(byseason_df):
    season_dict = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
    byseason_df['season'] = byseason_df['season'].map(season_dict)
    byseason = byseason_df.assign(cnt_k=lambda x: x['cnt'] / 1000)
    return byseason

def by_registered(registeredbymonth_df):
    monthly_data = registeredbymonth_df.groupby(['year', 'month']).agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return monthly_data

byseason_df = pd.read_csv("https://raw.githubusercontent.com/nisrina-ris/proyek_analisis_data/main/dashboard/byseason.csv")
registeredbymonth_df = pd.read_csv("https://raw.githubusercontent.com/nisrina-ris/proyek_analisis_data/main/dashboard/monthly_data.csv")


by_season_df = by_season(byseason_df)

# Convert 'year' column to datetime type
registeredbymonth_df['year'] = pd.to_datetime(registeredbymonth_df['year'], format='%Y')

# Now you can use the .dt accessor
monthly_data_2011 = by_registered(registeredbymonth_df[registeredbymonth_df['year'].dt.year == 2011])
monthly_data_2012 = by_registered(registeredbymonth_df[registeredbymonth_df['year'].dt.year == 2012])

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