# MySQL
!pip install mysql-connector-python
!pip install pymysql
!pip install cryptography

#Streamlit
!pip install streamlit -q
!pip install streamlit_option_menu
!pip install streamlit-player

# Github Cloning
!git clone https://github.com/PhonePe/pulse.git

import json
import pandas as pd

#SQL Library
import mysql.connector
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

#Data Viz Libraries
import plotly.express as px
import plotly.io as pio

# ----------------------Aggregrated Transaction Data---------------------------#

path='/content/pulse/data/aggregated/transaction/country/india/state/'
Agg_state_list=os.listdir(path)

clm1={'State':[], 'Year':[],'Quarter':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm1['Transaction_type'].append(Name)
              clm1['Transaction_count'].append(count)
              clm1['Transaction_amount'].append(amount)
              clm1['State'].append(i)
              clm1['Year'].append(j)
              clm1['Quarter'].append(int(k.strip('.json')))

#Aggregrated Transaction dataframe
agg_trans=pd.DataFrame(clm1)

# Data cleaning
agg_trans.head()
agg_trans.isnull().sum()

# ----------------------Aggregrated User Data---------------------------#

path='/content/pulse/data/aggregated/user/country/india/state/'
Agg_state_list=os.listdir(path)

clm2={'State':[], 'Year':[],'Quarter':[],'Brand':[], 'Count':[], 'Percentage':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr_list = os.listdir(p_i)
    for j in Agg_yr_list:
        p_j=p_i+j+"/"
        Agg_qtr_list=os.listdir(p_j)
        for k in Agg_qtr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            try:
                for z in D['data']['usersByDevice']:
                   clm2['Brand'].append(z['brand'])
                   clm2['Count'].append(z['count'])
                   clm2['Percentage']=(z['percentage'])
                   clm2['State'].append(i)
                   clm2['Year'].append(j)
                   clm2['Quarter'].append(int(k.strip(".json")))
            except:
              pass

# Aggregrated user dataframe
agg_user= pd.DataFrame(clm2)

# Data cleaning
agg_user.head()
agg_user.isnull().sum()

# ----------------------Map Transaction Data---------------------------#

path='/content/pulse/data/map/transaction/hover/country/india/state/'
Map_state_list=os.listdir(path)

clm3={'State':[], 'Year':[],'Quarter':[],'District':[], 'Count':[], 'Amount':[]}

for i in Map_state_list:
  p_i = path+i+'/'
  Map_yr_list=os.listdir(p_i)
  for j in Map_yr_list:
    p_j=p_i+j+'/'
    Map_qtr_list=os.listdir(p_j)
    for k in Map_qtr_list:
      p_k=p_j+k
      data=open(p_k,'r')
      D=json.load(data)
      for z in D['data']['hoverDataList']:
        name=z['name']
        count=z['metric'][0]['count']
        amount=z['metric'][0]['amount']
        clm3['District'].append(name)
        clm3['Count'].append(count)
        clm3['Amount'].append(amount)
        clm3['State'].append(i)
        clm3['Year'].append(j)
        clm3['Quarter'].append(int(k.strip('.json')))

# Map Transaction Dataframe
map_trans=pd.DataFrame(clm3)

# Data cleaning
map_trans.head()
map_trans.isnull().sum()

# ----------------------Map User Data---------------------------#

path='/content/pulse/data/map/user/hover/country/india/state/'
Map_state_list=os.listdir(path)

clm4={'State':[], 'Year':[],'Quarter':[],'District':[], 'Users':[]}

for i in Map_state_list:
  p_i=path+i+'/'
  Map_yr_list=os.listdir(p_i)
  for j in Map_yr_list:
    p_j=p_i+j+'/'
    Map_qtr_list=os.listdir(p_j)
    for k in Map_qtr_list:
      p_k=p_j+k
      data =open(p_k,'r')
      d=json.load(data)
      for z, values in d['data']['hoverData'].items():
        users=values['registeredUsers']
        dist=z
        clm4['State'].append(i)
        clm4['Year'].append(j)
        clm4['Quarter'].append(int(k.strip('.json')))
        clm4['District'].append(dist)
        clm4['Users'].append(users)

# Map User Dataframe
map_user=pd.DataFrame(clm4)

# Data cleaning

map_user.head()
map_user.isnull().sum()

# ----------------------Top Transaction Data---------------------------#

path='/content/pulse/data/top/transaction/country/india/state/'
Top_state_list=os.listdir(path)

clm5={'State':[], 'Year':[],'Quarter':[],'District':[], 'Count':[], 'Amount':[]}

for i in Top_state_list:
  p_i=path+i+'/'
  Top_yr_list=os.listdir(p_i)
  for j in Top_yr_list:
    p_j=p_i+j+'/'
    Top_qtr_list=os.listdir(p_j)
    for k in Top_qtr_list:
      p_k=p_j+k
      data =open(p_k,'r')
      d=json.load(data)
      for z in d['data']['districts']:
        cnt=z['metric']['count']
        amount=z['metric']['amount']
        name=z['entityName']
        clm5['State'].append(i)
        clm5['Year'].append(j)
        clm5['Quarter'].append(int(k.strip('.json')))
        clm5['District'].append(name)
        clm5['Count'].append(cnt)
        clm5['Amount'].append(amount)

# Top Transaction dataframe
top_trans=pd.DataFrame(clm5)

# Data cleaning
top_trans.head()
top_trans.isnull().sum()

# ----------------------Top User Data---------------------------#

path='/content/pulse/data/top/user/country/india/state/'
Top_state_list=os.listdir(path)

clm6={'State':[], 'Year':[],'Quarter':[],'District':[], 'Users':[]}

for i in Top_state_list:
      p_i=path+i+'/'
      Top_yr_list=os.listdir(p_i)
      for j in Top_yr_list:
        p_j=p_i+j+'/'
        Top_qtr_list=os.listdir(p_j)
        for k in Top_qtr_list:
           p_k=p_j+k
           data =open(p_k,'r')
           d=json.load(data)
           for z in d['data']['districts']:
             name=z['name']
             users=z['registeredUsers']
             clm6['State'].append(i)
             clm6['Year'].append(j)
             clm6['Quarter'].append(int(k.strip('.json')))
             clm6['District'].append(name)
             clm6['Users'].append(users)

# Top User dataframe
top_user=pd.DataFrame(clm6)

# Data Cleaning
top_user.head()
top_user.isnull().sum()


#---------------------------------Converting all dataframes to CSV files---------------------------------#
agg_trans.to_csv('agg_transactions.csv',index=False)
agg_user.to_csv('agg_users.csv',index=False)
map_trans.to_csv('map_transactions.csv',index=False)
map_user.to_csv('map_users.csv',index=False)
top_trans.to_csv('top_transactions.csv',index=False)
top_user.to_csv('top_users.csv',index=False)

# ---------------Data Migration to MySQL------------------#

#credentials to connect to the database using ngrok
host='0.tcp.in.ngrok.io'
port= **port number**
user='root'
password= **your password**
charset='utf8'
database='phonepe'

#--------------------Connection from Google colab to local MySql Server----------------#
engine=create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
con=engine.connect()

agg_trans_df=pd.read_csv(r'/content/agg_transactions.csv')
agg_trans_df.to_sql('agg_trans',engine,if_exists='replace')

agg_user_df=pd.read_csv(r'/content/agg_users.csv')
agg_user_df.to_sql('agg_users',engine,if_exists='replace')

map_trans_df=pd.read_csv(r'/content/map_transactions.csv')
map_trans_df.to_sql('map_trans', engine, if_exists='replace')

map_user_df=pd.read_csv(r'/content/map_users.csv')
map_user_df.to_sql('map_users', engine, if_exists='replace')

top_trans_df=pd.read_csv(r'/content/top_transactions.csv')
top_trans_df.to_sql('top_trans', engine, if_exists='replace')

top_users_df=pd.read_csv(r'/content/top_users.csv')
top_users_df.to_sql('top_users', engine, if_exists='replace')

#-------------Query Execution----------------#
conn = pymysql.connect(
      host='0.tcp.in.ngrok.io',
      port= **port number**,
      user='root',
      password= **your password**,
      charset='utf8',
      database='phonepe'
          )
cursor = conn.cursor()

# --------Page Setup----------#
st.set_page_config(page_title = "PhonePe Pulse",layout="wide")
with open('/content/style.css') as f:
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
if choice=='Home':
  col1,col2 = st.columns(2)
  with col1:
      st.image('/content/logo.svg', width=350)
  with col2:
      st.title(":violet[Pulse Data Visualization]")
  st.markdown("The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.")
  st_player("https://www.youtube.com/watch?v=c_1H6vivsiA&embeds_euri=https%3A%2F%2Fwww.phonepe.com%2F&feature=emb_imp_woyt")
  st.subheader(":violet[Powered by]")
  col1,col2 = st.columns(2)
  with col1:
      st.image('/content/phonepe_home.png',)
  with col2:
      st.header(":violet[App developed by]")
      st.header(":violet[Your Name]")
if choice=='Explore Data':
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

  mt['State'] = mt['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunanchal Pradesh',
       'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
       'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
       'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
       'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
       'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
       'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
       'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana','tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
       'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})
  mu['State'] = mu['State'].replace({'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh':'Andhra Pradesh', 'arunachal-pradesh':'Arunanchal Pradesh',
          'assam':'Assam', 'bihar':'Bihar', 'chandigarh':'Chandigarh', 'chhattisgarh':'Chhattisgarh',
          'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli and Daman and Diu', 'delhi': 'Delhi', 'goa':'Goa', 'gujarat': 'Gujarat',
          'haryana':'Haryana','himachal-pradesh':'Himachal Pradesh', 'jammu-&-kashmir':'Jammu & Kashmir', 'jharkhand':'Jharkhand',
          'karnataka':'Karnataka', 'kerala':'Kerala', 'ladakh':'Ladakh', 'lakshadweep':'Lakshadweep', 'madhya-pradesh':'Madhya Pradesh',
          'maharashtra':'Maharashtra', 'manipur':'Manipur', 'meghalaya':'Meghalaya', 'mizoram':'Mizoram', 'nagaland':'Nagaland',
          'odisha':'Odisha', 'puducherry':'Puducherry', 'punjab':'Punjab', 'rajasthan':'Rajasthan', 'sikkim':'Sikkim',
          'tamil-nadu': 'Tamil Nadu', 'telangana':'Telangana','tripura':'Tripura', 'uttar-pradesh':'Uttar Pradesh',
          'uttarakhand':'Uttarakhand', 'west-bengal':'West Bengal'})

  if selected == "Transactions":
    df1 = mt.groupby(['State', 'Year', 'Quarter'], as_index=False).sum(numeric_only=True)
    df1 = df1.query(f"Year == {year} & Quarter == {quarter}")
    df1 = df1[['State', 'Amount']]

    fig1 = px.choropleth(df1,
                          geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                          featureidkey='properties.ST_NM',
                          locations='State',
                          color='Amount',
                          hover_data=['State', 'Amount'],
                          projection="robinson",
                          color_continuous_scale='Plasma_r',
                          range_color=(12, 0))
    fig1.update_geos(fitbounds='locations', visible=False)
    fig1.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    col1,col2,col3=st.columns(3)
    with col1:
      st.plotly_chart(fig1)
    with col3:
      st.write(df1)

  if selected == "Users":
    df3 = mu.groupby(['State','Year','Quarter'], as_index=False).sum(numeric_only=True)
    df3 = df3.query(f"Year =={year} & Quarter =={quarter}")
    df3 = df3[['State', 'Users']]

    fig3 = px.choropleth(df3,
                          geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                          featureidkey='properties.ST_NM',
                          locations='State',
                          color='Users',
                          hover_data=['State', 'Users'],
                          color_continuous_scale='Viridis_r',
                          range_color=(12, 0))
    fig3.update_geos(fitbounds='locations', visible=False)
    fig3.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    col1,col2,col3=st.columns(3)
    with col1:
      st.plotly_chart(fig3)
    with col3:
      st.write(df3)

if choice =="Insights":
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
  conn.close()
  # DOWNLOAD REPORT
  st.subheader(":violet[The Annual Report of Phonepe Pulse data]")
  st.markdown("[DOWNLOAD REPORT](https://www.phonepe.com/pulsestatic/732/pulse/static/83bc2c9e9038369af2eb9eb7d62cb49f/PhonePe_Pulse_BCG_report.pdf)")

    
                   ******************************************* END **********************************************
