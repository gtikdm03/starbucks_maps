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


path = os.path.join(os.path.expanduser('~'),'Desktop/')
file_name = 'starbucks_information.xlsx'

def starbucks_crawling():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    columns= ['매장명', '위도', '경도', '매장타입', '주소', '전화번호']
    starbucks_info = []
    url = 'https://www.starbucks.co.kr/store/store_map.do'
    driver.get(url)
    time.sleep(3)
    local_button = driver.find_element(By.CSS_SELECTOR, '#container > div > form > fieldset > div > section > article.find_store_cont > article > header.loca_search > h3 > a').click()
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    all_local = soup.select('#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li')
    for i in range(1,len(all_local)+1):
        local = all_local[i-1].text
        loc_button = driver.find_element(By.CSS_SELECTOR, '#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child({}) > a'.format(i)).click()
        time.sleep(5)
        # Skip clicking all_find_button if i is 17
        if i != 17:
            all_find_button = driver.find_element(By.CSS_SELECTOR, '#mCSB_2_container > ul > li:nth-child(1) > a.set_gugun_cd_btn').click()
            time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        starbucks_list = soup.select('#mCSB_3_container > ul > li')
        rank=0
        for starbucks in starbucks_list:
            starbucks_name = starbucks.select('strong')[0].text
            lat = starbucks['data-lat']
            lng = starbucks['data-long']
            store_type = starbucks.select('i')[0].text
            address = starbucks.select('p')[0].get_text(separator='\n').split('\n')[0].strip()
            tel = starbucks.select('p')[0].get_text(separator='\n').split('\n')[1].strip()
            starbucks_info.append((starbucks_name, lat, lng, store_type, address, tel))
            starbucks_df = pd.DataFrame(starbucks_info, columns=columns)
            starbucks_df.to_excel(path + file_name, index=False)
            rank+=1
            print('{}번째 매장 크롤링 완료!'.format(rank))
        print('{}지역의 크롤링이 완료되었습니다.'.format(local))
        local_searching = driver.find_element(By.CSS_SELECTOR, '#container > div > form > fieldset > div > section > article.find_store_cont > article > header.loca_search').click()
        time.sleep(1)

def run_make_starbucks_map():
    starbucks_data = pd.read_excel(path + file_name)
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
    
    # Streamlit code to display the map using streamlit_folium
    st.title("Starbucks Locations Map")  # Add a title
    st.markdown("Here are the locations of Starbucks stores.")
    st_folium.folium_static(starbucks_maps, height=600)  # Directly display the map without saving as HTML

#######################################################함수######################################
#starbucks_crawling()
run_make_starbucks_map()




