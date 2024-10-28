from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import folium
from folium.plugins import MarkerCluster
import streamlit as st  # Add this import at the top of your file
import streamlit_folium as st_folium  # Ensure this import is present

starbucks_data = pd.read_excel('starbucks_information.xlsx')
starbucks_maps = folium.Map(location=[35.90113674141647, 127.97481460691101], zoom_start=7)
marker_cluster = MarkerCluster().add_to(starbucks_maps)
for name, lat, lng in zip(starbucks_data['매장명'], starbucks_data['위도'], starbucks_data['경도']):
    marker = folium.Marker([lat, lng],
                           popup=name,
                           icon=folium.Icon('green', icon='star'),
                           radius=10,
                           color='green',
                           fill=True,
                           fill_color='green',
                           fill_opacity=0.7
                           ).add_to(marker_cluster)  # Add marker to the MarkerCluster

st.title("Starbucks Locations Map")  # Add a title
st.markdown("Here are the locations of Starbucks stores.")
st_folium.folium_static(starbucks_maps, height=600)  # Directly display the map without saving as HTML
