
import json
import pandas as pd
import numpy as np

#SQL Library
import mysql.connector as sql
import sqlalchemy
from sqlalchemy import create_engine,text
import sqlalchemy.types as sqltypes
import pymysql

#OS Library
import os

#User Interface (Web App)
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_player import st_player
from PIL import Image

#Data Viz Libraries
import plotly.express as px
import plotly.io as pio



# ---------------Creating connection with MySQL Workbench-----------------#
mydb = sql.connect(
    host="127.0.0.1",
    user="root",
    password="abarna16",
    port=3306,
    database="phonepe")
cursor = mydb.cursor(buffered=True)


# ----------------About page--------------#
def home_page():
    col1,col2 = st.columns(2)
    with col1:
        st.image('C:/Users/abarn/OneDrive/Documents/GUVI_Projects/PhonePe_Pulse_Data_Visualization/Images and demo/logo.svg', width=350)
    with col2:
        st.title(":violet[Pulse Data Visualization]")
    st.markdown("The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.")
    st_player("https://www.youtube.com/watch?v=c_1H6vivsiA&embeds_euri=https%3A%2F%2Fwww.phonepe.com%2F&feature=emb_imp_woyt")
    st.subheader(":violet[Powered by]")
    col1,col2 = st.columns(2)
    with col1:
        col1.image(Image.open("C:/Users/abarn/OneDrive/Documents/GUVI_Projects/PhonePe_Pulse_Data_Visualization/Images and demo/phonepe_home.png"))
    with col2:
        st.header(":violet[App developed by]")
        st.header(":violet[ABARNA S]")
    

#----------------------Explore Data page-------------------#
def explore_data_page():
  
  st.title(':violet[Explore Data across India]')
  st.subheader(':violet[PhonePe Pulse | The beat of Progress]',divider='gray')
  col1, col2, col3 = st.columns(3)
  with col1:
    selected=st.selectbox(':violet[ALL INDIA]',('Transactions','Users'))
  with col2:
    year=st.selectbox(':violet[YEAR]',['2018','2019','2020','2021','2022','2023'])
  with col3:
    quarter=st.selectbox(':violet[QUARTER]',('1','2','3','4'))
  def data_fetching():

    cursor.execute("SELECT * FROM phonepe.map_trans")
    myresult3 = cursor.fetchall()
    mt = pd.DataFrame(myresult3, columns=['id', 'State', 'Year', 'Quarter', 'District', 'Count', 'Amount'])

    cursor.execute("SELECT * FROM phonepe.map_users")
    myresult4 = cursor.fetchall()
    mu = pd.DataFrame(myresult4, columns=['id', 'State', 'Year', 'Quarter', 'District', 'Users'])

    return  mt, mu

  mt, mu = data_fetching()

  
  
  if selected == "Transactions":
    cursor.execute( f"select State, Sum(Transaction_amount) as Amount from agg_trans where Year={year} and Quarter={quarter} group by State;")
    result = cursor.fetchall()
    df1 = pd.DataFrame(result, columns=['State', 'Amount'])
    df1['State'] = df1['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunanchal Pradesh',
       'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
       'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
       'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
       'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
       'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
       'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana','tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
       'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})
    
    fig1 = px.choropleth(df1,
                          geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                          featureidkey='properties.ST_NM',
                          locations='State',
                          color='Amount',
                          hover_data=['State', 'Amount'],
                          projection="robinson",
                          color_continuous_scale='Plasma_r',
                          title="Transaction Data",
                          range_color=(12, 0))
    fig1.update_geos(fitbounds='locations', visible=False)
    fig1.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
    fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    col1,col2,col3=st.columns(3)
    with col1:
      st.plotly_chart(fig1)
    with col3:
      st.write(df1)

  if selected == "Users":
    cursor.execute( f"select State, cast(sum(Users) as DECIMAL) as Users from map_users where Year={year} and Quarter={quarter} group by State;")
    result = cursor.fetchall()
    df2 = pd.DataFrame(result, columns=['State', 'Users'])
    df2['State'] = df2['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunanchal Pradesh',
          'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
          'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
          'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
          'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
          'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
          'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
          'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana','tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
          'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})
    fig2 = px.choropleth(df2,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='State',
                        hover_data=['State', 'Users'],
                        projection="miller",
                        color_continuous_scale='viridis_r',
                        range_color=(12, 0))
    fig2.update_geos(fitbounds='locations', visible=False)
    fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    col1,col2,col3=st.columns(3)
    with col1:
      st.plotly_chart(fig2)
    with col3:
      st.write(df2)
      

#-----------------Analysis Page-----------------------#
def insights_page():
   st.title(":violet[Top Insights from the Data]")
   options = ["--select--",
            "Top 10 states based on amount of transaction of all years",
            "Least 10 states based on amount of transaction of all years",
            "Top 10 States and Districts based on Registered_users",
            "Least 10 States and Districts based on Registered_users",
            "Top 10 Districts based on the Transaction Amount",
            "Least 10 Districts based on the Transaction Amount",
            "Top 10 Districts based on the number of Transactions",
            "Least 10 Districts based on the number of Transactions",
            "Top Transaction types based on the Transaction Amount",
            "Top 10 Mobile Brands based on the No of transactions by User"]
   select = st.selectbox(":violet[Select the option]",options)

   # Query 1
   if select == "Top 10 states based on amount of transaction of all years":
      cursor.execute(
          "SELECT DISTINCT State,Year, SUM(Amount) AS Total_Transaction_Amount FROM top_trans GROUP BY State,Year ORDER BY Total_Transaction_Amount DESC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['States', 'Year', 'Transaction_amount']
      df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Top 10 states based on amount of transaction]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig= px.bar(df, x='States', y='Transaction_amount', text_auto='.2s', title="Top 10 states based on amount of transaction", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)

   # Query 2
   elif select == "Least 10 states based on amount of transaction of all years":
      cursor.execute(
          "SELECT DISTINCT State,Year, SUM(Amount) as Total_Transaction_Amount FROM top_trans GROUP BY State, Year ORDER BY Total_Transaction_Amount ASC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['States', 'Year', 'Transaction_amount']
      df = pd.DataFrame(data, columns=columns, index=range(1,len(data)+1))
      st.subheader(":violet[Least 10 states based on amount of transaction]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig = px.bar(df, x='States', y='Transaction_amount', text_auto='.2s', title="Least 10 states based on amount of transaction", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)

   # Query 3
   elif select == "Top 10 States and Districts based on Registered_users":
      cursor.execute("SELECT DISTINCT State, SUM(Users) AS Users FROM top_users GROUP BY State ORDER BY Users DESC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['State','Registered_users']
      df1 = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Top 10 State based on Registered_users]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df1)
      with col2:
        fig = px.bar(df1, x='State', y='Registered_users', text_auto='.2s', title="Top 10 States based on Registered_users" )
        fig.update_traces(textfont_size=14,marker_color='#F8CD47')
        fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
        st.plotly_chart(fig,use_container_width=True)


      cursor.execute("SELECT DISTINCT District, SUM(Users) AS Users FROM top_users GROUP BY District ORDER BY Users DESC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['State','Registered_users']
      df2 = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Top 10 Districts based on Registered_users]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df2)
      with col2:
        fig = px.bar(df2, x='State', y='Registered_users', text_auto='.2s', title="Top 10 Districts based on Registered_users", )
        fig.update_traces(textfont_size=14,marker_color='#F8CD47')
        fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
        st.plotly_chart(fig,use_container_width=True)


   # Query 4
   elif select == "Least 10 States and Districts based on Registered_users":
      cursor.execute("SELECT DISTINCT State, SUM(Users) AS Users FROM top_users GROUP BY State ORDER BY Users ASC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['State','Registered_users']
      df1 = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Least 10 States based on Registered_users]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df1)
      with col2:
          fig = px.bar(df1, x='State', y='Registered_users', text_auto='.2s', title="Least 10 State based on Registered_users", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)

      cursor.execute("SELECT DISTINCT District, SUM(Users) AS Users FROM top_users GROUP BY District ORDER BY Users ASC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['District','Registered_users']
      df2 = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Least 10 Districts based on Registered_users]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df2)
      with col2:
          fig = px.bar(df2, x='District', y='Registered_users', text_auto='.2s', title="Least 10 Districts based on Registered_users", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)


   # Query 5
   elif select == "Top 10 Districts based on the Transaction Amount":
      cursor.execute("SELECT DISTINCT District,State, SUM(Amount) AS Total_Transaction_Amount FROM map_trans GROUP BY State, District ORDER BY Total_Transaction_Amount DESC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['District','States', 'Amount']
      df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Top 10 Districts based on Transaction Amount]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig = px.bar(df, x='District', y='Amount', text_auto='.2s', title="Top 10 Districts based on the Transaction Amount", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)

   # Query 6
   elif select == "Least 10 Districts based on the Transaction Amount":
      cursor.execute(
          "SELECT DISTINCT District,State, SUM(Amount) AS Total_Transaction_Amount FROM map_trans GROUP BY State, District ORDER BY Total_Transaction_Amount ASC LIMIT 10;");
      data = cursor.fetchall()
      columns =['District','States', 'Amount']
      df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Least 10 Districts based on Transaction Amount]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig = px.bar(df, x='District', y='Amount', text_auto='.2s', title="Least 10 Districts based on the Transaction Amount", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)

   # Query 7
   elif select == "Top 10 Districts based on the number of Transactions":
      cursor.execute(
          "SELECT DISTINCT District,State, SUM(Count) AS No_of_Transactions FROM map_trans GROUP BY State, District ORDER BY No_of_Transactions DESC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['District', 'States', 'Count']
      df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Top 10 Districts based on the number of Transactions]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig = px.bar(df, x='District', y='Count', text_auto='.2s', title="Top 10 Districts based on number of Transactions", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)

   # Query 8
   elif select == "Least 10 Districts based on the number of Transactions":
      cursor.execute(
          "SELECT DISTINCT District,State, SUM(Count) AS No_of_Transactions FROM map_trans GROUP BY State, District ORDER BY No_of_Transactions ASC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['District', 'States', 'Count']
      df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Least 10 Districts based on the number of Transactions]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig = px.bar(df, x='District', y='Count', text_auto='.2s', title="Least 10 Districts based on number of Transactions" )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)


   # Query 9
   elif select == "Top Transaction types based on the Transaction Amount":
      cursor.execute(
          "SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM agg_trans GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5;");
      data = cursor.fetchall()
      columns = ['Transaction_type', 'Transaction_amount']
      df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Top Transaction Types based on the Transaction Amount]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig = px.bar(df, x='Transaction_type', y='Transaction_amount', text_auto='.2s', title="Top Transaction types based on the Transaction Amount", )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)

   # Query 10
   elif select == "Top 10 Mobile Brands based on the No of transactions by User":
      cursor.execute(
          "SELECT DISTINCT Brand, SUM(Count) as Total FROM agg_users GROUP BY Brand ORDER BY Total DESC LIMIT 10;");
      data = cursor.fetchall()
      columns = ['Brands', 'User_Count']
      df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
      st.subheader(":violet[Top 10 Mobile Brands based on User count of transaction]")
      col1, col2 = st.columns(2)
      with col1:
          st.write(df)
      with col2:
          fig = px.bar(df, x='Brands', y='User_Count', text_auto='.2s', title="Top 10 Mobile Brands based on the No of transactions by User" )
          fig.update_traces(textfont_size=14,marker_color='#F8CD47')
          fig.update_layout(title_font_color='#000000 ',title_font=dict(size=20))
          st.plotly_chart(fig,use_container_width=True)
   
   # DOWNLOAD REPORT
   st.subheader(":violet[The Annual Report of Phonepe Pulse data]")
   st.markdown("[DOWNLOAD REPORT](https://www.phonepe.com/pulsestatic/732/pulse/static/83bc2c9e9038369af2eb9eb7d62cb49f/PhonePe_Pulse_BCG_report.pdf)")


#----------------------PAGE SETUP---------------------#
def main():
    st.set_page_config(page_title = "PhonePe Pulse",layout="wide")
    with open('C:/Users/abarn/OneDrive/Documents/GUVI_Projects/PhonePe_Pulse_Data_Visualization/style.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    with st.sidebar:
        choice=option_menu(None,['Home','Explore Data','Insights'],
                    icons=["house-door-fill","database-fill","bar-chart-fill"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "25px", "text-align": "centre", "margin": "0px",
                                                "--hover-color": "#e9d6ff"},
                                   "icon": {"font-size": "25px"},
                                   "container" : {"max-width": "3800px"},
                                   "nav-link-selected": {"background-color": "#391c59","color":"#ffffff"}})
    if choice == "Home":
        home_page()
    elif choice == "Explore Data":
        explore_data_page()
    elif choice == "Insights":
        insights_page()
    

if __name__ == "__main__":
    main()





