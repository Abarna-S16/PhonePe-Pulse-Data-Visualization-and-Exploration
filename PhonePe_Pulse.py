#!/usr/bin/env python
# coding: utf-8

# In[22]:


import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector as sql
from mysql.connector import connection
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import requests
import json


# In[23]:


# ---------------Creating connection with MySQL Workbench-----------------#
mydb = sql.connect(
    host="127.0.0.1",
    user="root",
    password="abarna16",
    port=3306,
    database="phonepe")
cursor = mydb.cursor(buffered=True)


# In[28]:


# ----------------About page--------------#
def home_page():
    col1,col2 = st.columns(2)
    with col1:
        st.image('C:/Users/abarn/OneDrive/Documents/GUVI_Projects/PhonePe_Pulse_Data_Visualization/Images and demo/logo.svg', width=350)
    with col2:
        st.title(":violet[Pulse Data Visualization]")
    st.markdown("The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.")
    st.video("C:/Users/abarn/OneDrive/Documents/GUVI_Projects/PhonePe_Pulse_Data_Visualization/Introducing PhonePe Pulse.mp4")
    st.subheader(":violet[Powered by]")
    col1,col2 = st.columns(2)
    with col1:
        st.image("C:/Users/abarn/OneDrive/Documents/GUVI_Projects/PhonePe_Pulse_Data_Visualization/Images and demo/phonepe_home.png")
    with col2:
        st.header(":violet[App developed by]")
        st.header(":violet[ABARNA S]")
    


# In[29]:


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
        analysis_page()
    elif choice == "Insights":
        insights_page()
    

if __name__ == "__main__":
    main()


# In[ ]:




