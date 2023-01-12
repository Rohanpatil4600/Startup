import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title = 'StartUp Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors = 'coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis ')
    total = round(df['amount'].sum())
    max_funding=round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0])
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    num_startup = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max Funding', str(max_funding) + 'Cr')
    with col3:
        st.metric('Average Funding', str(avg_funding) + 'Cr')
    with col4:
        st.metric('Funded StartUps', str(num_startup))
    st.header('MoM graph')
    selected_option =  st.selectbox('select Type',['Total', 'Count'])
    if selected_option== 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x-axis'] = temp_df['month'].astype(str) + '-' + temp_df['amount'].astype(str)
    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x-axis'], temp_df['amount'])
    st.pyplot(fig6)






def load_investor_details(investor):
    st.title(investor)
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Last 5 investments')
    st.dataframe(last5_df)
    col1, col2 = st.columns(2)
    with col1:
        big_series =df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax= plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        ver_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('sector invested in ')
        fig1, ax1 = plt.subplots()
        ax1.pie (ver_series, labels= ver_series.index, autopct = "%0.01f%%")
        st.pyplot(fig1)

    col3, col4 =  st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('round invested in ')
        fig2, ax2 = plt.subplots()
        ax2.pie (round_series, labels= round_series.index, autopct = "%0.01f%%")
        st.pyplot(fig2)
    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('city invested in ')
        fig3, ax3 = plt.subplots()
        ax3.pie (city_series, labels= city_series.index, autopct = "%0.01f%%")
        st.pyplot(fig3)

    df['year']=df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('Year on year investment ')
    fig5, ax5 = plt.subplots()
    ax5.plot(year_series.index,year_series.values)
    st.pyplot(fig5)



st.sidebar.title('StartUp Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('select startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Analysis')
    st.title('StartUp Analysis')
else:
    selected_investor = st.sidebar.selectbox('select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Analysis')
    if btn2:
        load_investor_details(selected_investor)
