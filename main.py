import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set Layout
st.set_page_config(layout="wide")

# Import Dataset
df_hour = pd.read_csv('dataset/hour.csv')
df_day = pd.read_csv('dataset/day.csv')

# Convert 'dteday' to datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'], errors='coerce')
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'], errors='coerce')

# Date Filter Section
st.sidebar.header('Date Filter')
start_date = st.sidebar.date_input('Start date', df_day['dteday'].min())
end_date = st.sidebar.date_input('End date', df_day['dteday'].max())

# Filter data based on date range
filtered_df_day = df_day[(df_day['dteday'] >= pd.to_datetime(start_date)) & (df_day['dteday'] <= pd.to_datetime(end_date))]
filtered_df_hour = df_hour[(df_hour['dteday'] >= pd.to_datetime(start_date)) & (df_hour['dteday'] <= pd.to_datetime(end_date))]

# Define functions to process the data
def create_avg_user_month(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt', 'dteday'], inplace=True)
    df['mnth'] = df['dteday'].dt.month  # Create 'mnth' 
    return df.groupby('mnth').agg({'cnt': 'mean'}).reset_index()

def create_sum_user_day(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt'], inplace=True)
    return df.groupby(df['dteday'].dt.day).agg({'cnt': 'sum'}).reset_index()

def create_sum_user_day(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt'], inplace=True)
    return df.groupby(df['dteday'].dt.day).agg({'cnt': 'sum'}).reset_index()

def create_avg_hr_days(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt'], inplace=True)
    return df.groupby(['hr', 'weekday']).agg({'cnt': 'mean'}).reset_index()

def create_sum_user_season(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt'], inplace=True)
    return df.groupby('season').agg({'cnt': 'sum'}).reset_index()

def create_avg_user_season(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt'], inplace=True)
    return df.groupby('season').agg({'cnt': 'mean'}).reset_index()

def create_avg_user_reg(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt'], inplace=True)
    return df.groupby('registered').agg({'cnt': 'mean'}).reset_index()

def create_avg_user_cas(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df.dropna(subset=['cnt'], inplace=True)
    return df.groupby('casual').agg({'cnt': 'mean'}).reset_index()

def create_monthly_user(df):
    df['cnt'] = pd.to_numeric(df['cnt'], errors='coerce')
    df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')
    df.dropna(subset=['cnt', 'dteday'], inplace=True)
    return df.groupby(df['dteday'].dt.to_period('M')).agg({'cnt': 'sum'}).reset_index()

# Create Data with Filtered Dataset
avg_user_month = create_avg_user_month(filtered_df_day)
sum_user_day = create_sum_user_day(filtered_df_day)
sum_user_day = create_sum_user_day(filtered_df_day)
avg_hr_days = create_avg_hr_days(filtered_df_hour)
sum_user_season = create_sum_user_season(filtered_df_day)
avg_user_season = create_avg_user_season(filtered_df_day)
avg_user_reg = create_avg_user_reg(filtered_df_hour)
avg_user_cas = create_avg_user_cas(filtered_df_hour)
monthly_user = create_monthly_user(filtered_df_day)

# Convert period back to datetime for plotting
monthly_user['dteday'] = monthly_user['dteday'].dt.to_timestamp()

# Debugging: Print out the first few rows and types of the DataFrames
print("Monthly User Data:")
print(monthly_user.head())
print("Columns and types:")
print(monthly_user.dtypes)

# Visualization
st.image('gowessantai.png')

st.header('Bike Sharing Analysis ')

# Metrics Section
col1, col2, col3 = st.columns(3)
with col1:
    total_users = filtered_df_day['cnt'].sum()
    st.metric('Total Users', f"{total_users:,}")
with col2:
    user_2011 = filtered_df_day[filtered_df_day['yr'] == 0]['cnt'].sum()
    st.metric('Users in 2011', f"{user_2011:,}")
with col3:
    user_2012 = filtered_df_day[filtered_df_day['yr'] == 1]['cnt'].sum()
    st.metric('Users in 2012', f"{user_2012:,}", '64.9%')

# Monthly Users Section
st.subheader('Monthly Users')
col1, col2 = st.columns([1, 1])  # Pastikan proporsi kolom sama

with col1:
    # Plot grafik pertama dengan ukuran yang ditetapkan
    fig1, ax1 = plt.subplots(figsize=(8, 6))  # Menentukan ukuran canvas yang sama
    try:
        sns.lineplot(data=monthly_user, x='dteday', y='cnt', marker='o', ax=ax1)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        fig1.autofmt_xdate()
        ax1.set_title('Monthly Users (2011-2012)', fontsize=16)
        ax1.set_xlabel(None)
        ax1.set_ylabel('Total Users', fontsize=12)
        st.pyplot(fig1)
    except Exception as e:
        st.error(f"Error in plotting monthly users: {e}")

with col2:
    # Plot grafik kedua dengan ukuran yang sama
    fig2, ax2 = plt.subplots(figsize=(8, 6))  # Pastikan ukuran yang sama untuk uniformitas
    try:
        sns.barplot(data=avg_user_month, x='mnth', y='cnt', hue='mnth', palette='Blues', errorbar=None, ax=ax2)
        ax2.legend_.remove()
        ax2.set_title("Peak Usage Month", fontsize=16)
        ax2.set_xlabel(None)
        ax2.set_ylabel('Avg Users', fontsize=12)
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Error in plotting avg user month: {e}")

        # Comparison between Weekdays and Weekends
st.subheader('Weekday vs Weekend Usage')

# Create 'day_of_week' column to indicate the day of the week (0 = Monday, 6 = Sunday)
filtered_df_day['day_of_week'] = filtered_df_day['dteday'].dt.dayofweek

# Create 'day_type' column to categorize weekdays and weekends
filtered_df_day['day_type'] = filtered_df_day['day_of_week'].apply(lambda x: 'Weekday' if x >= 5 else 'Weekend')

# Group by 'day_type' and calculate the average number of users
weekday_vs_weekend = filtered_df_day.groupby('day_type').agg({'cnt': 'mean'}).reset_index()

# Plot the comparison
fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.barplot(data=weekday_vs_weekend, x='day_type', y='cnt', palette="Blues", ax=ax3)
ax3.set_title('Comparison of Bike Rentals on Weekdays vs Weekends', fontsize=16)
ax3.set_xlabel('Day Type', fontsize=12)
ax3.set_ylabel('Average Users', fontsize=12)
st.pyplot(fig3)



# Daily Users Section
st.subheader('Daily Users')
fig, ax = plt.subplots(figsize=(10, 6))  
weekday_opt = ['All Days', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
option = st.selectbox('', weekday_opt, index=weekday_opt.index('All Days'))
try:
    if option != 'All Days':
        sns.lineplot(data=avg_hr_days[avg_hr_days['weekday'] == option], x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
        ax.set_title(f'{option} Busy Hour', fontsize=12)
    else:
        sns.lineplot(data=avg_hr_days, x='hr', y='cnt', marker='o', errorbar=None, ax=ax)
        ax.set_title('All Days Busy Hour', fontsize=12)
except Exception as e:
    st.error(f"Error in plotting daily users: {e}")

ax.set_xlabel(None)
ax.set_ylabel('Avg Users', fontsize=10)
ax.set_xticks(range(0, 24))
ax.set_ylim(avg_hr_days['cnt'].min() - 10, avg_hr_days['cnt'].max() + 10)
st.pyplot(fig)