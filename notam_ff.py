# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 12:20:21 2023

@author: dsanm
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WD
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import streamlit as st

api_key = st.secrets['at_token']
base_id = st.secrets['at_base_id']
table_name = 'vuelos_programados_notam'
headers_AT = {"Authorization" : f"Bearer {api_key}",  "Content-Type" : 'application/json' }
endpoint_AT = f'https://api.airtable.com/v0/{base_id}/{table_name}'
@st.cache_data
def get_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

def convert_to_dataframe(airtable_records):
    """Converts dictionary output from airtable_download() into a Pandas dataframe."""
    airtable_rows = []
    airtable_index = []
    for record in airtable_records['records']:
        airtable_rows.append(record['fields'])
        airtable_index.append(record['id'])
    airtable_dataframe = pd.DataFrame(airtable_rows, index=airtable_index)
    return airtable_dataframe

def wdec(selector):
    '''WD waits'''
    wdec_fun = WD(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    return wdec_fun
def dfe(selector):
    '''find element'''
    d_v = driver.find_elements(By.CSS_SELECTOR, selector)
    return d_v

at = requests.get(endpoint_AT,headers = headers_AT)
at.json()
atdf = convert_to_dataframe(at.json()).reset_index(drop=True)
pdgb = atdf.drop_duplicates(subset=['Coordenadas']).reset_index(drop=True)
b_1 = st.button('buscar notam')
if b_1:
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    exp_opt = ['enable-automation', 'enable-logging']
    chrome_options.add_experimental_option('excludeSwitches', exp_opt)
    prefs = {'profile.default_content_setting_values.notifications':1}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = get_driver()
    driver.get('https://drones.enaire.es/')
    
    wdec('body > div.cookiefirst-root.notranslate > div > div > div.cfAdwL.cf7ddU > div.cf2L3T.cfysV4.cf2mE1 > div.cf3Tgk.cf2pAE.cfAdwL.cf1IKf > div.cf1lHZ.cf2L3T > button').click()
    wdec('#widgets_Splash_Widget_30 > div.envelope > div:nth-child(2) > div.footer > div.jimu-btn.jimu-float-trailing.enable-btn').click()
    wdec('#scrollPreguntas > div:nth-child(2) > div.pregunta_respuesta.w3-col.s10.l6 > div > div > div:nth-child(2) > div').click()
    wdec('#esri_dijit_Search_0_input').send_keys('ciudad deportiva andres iniesta', Keys.ENTER)
    wdec('#widgets_CustomInfoClick_Widget_43 > div.esriPopup > div > div > a').click()
    wdec('#widgets_CustomInfoClick_Widget_43 > div.esriPopup > div > div > a').click()
    wdec('#widgets_CustomInfoClick_Widget_43_panel > div.title.jimu-panel-title.jimu-main-background > div.close-icon.jimu-float-trailing').click()
    wdec('#map_graphics_layer').click()
    wdec('#popupContent > div.AisosAlertas > div.mensajeDrones.NOTAM')
    alerts = dfe('#popupContent > div.AisosAlertas > div.mensajeDrones.NOTAM')
    for al in alerts:
        if '385804N 0015151W' in al.text:
            n_notam = al.text.split('\n')
            numero = n_notam[0]
    driver.quit()
    st.write('El número de notam de Albacete es:')
    st.write(numero)
b_2 = st.button('notam de vuelos')
if b_2:
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    exp_opt = ['enable-automation', 'enable-logging']
    chrome_options.add_experimental_option('excludeSwitches', exp_opt)
    prefs = {'profile.default_content_setting_values.notifications':1}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = get_driver()
    driver.get('https://drones.enaire.es/')
    
    wdec('body > div.cookiefirst-root.notranslate > div > div > div.cfAdwL.cf7ddU > div.cf2L3T.cfysV4.cf2mE1 > div.cf3Tgk.cf2pAE.cfAdwL.cf1IKf > div.cf1lHZ.cf2L3T > button').click()
    wdec('#widgets_Splash_Widget_30 > div.envelope > div:nth-child(2) > div.footer > div.jimu-btn.jimu-float-trailing.enable-btn').click()
    wdec('#scrollPreguntas > div:nth-child(2) > div.pregunta_respuesta.w3-col.s10.l6 > div > div > div:nth-child(2) > div').click()
    for i in range(len(pdgb)):
        
        wdec('#esri_dijit_Search_0_input').send_keys(pdgb.loc[i,'Coordenadas'], Keys.ENTER)        
        wdec('#widgets_CustomInfoClick_Widget_43 > div.esriPopup > div > div > a').click()
        wdec('#widgets_CustomInfoClick_Widget_43 > div.esriPopup > div > div > a').click()        
        wdec('#widgets_CustomInfoClick_Widget_43_panel > div.title.jimu-panel-title.jimu-main-background > div.close-icon.jimu-float-trailing').click()
        wdec('#map_graphics_layer').click()
        wdec('#popupContent > div.AisosAlertas')
        alerts = dfe('#popupContent > div.AisosAlertas > div.mensajeDrones.NOTAM')
        if len(alerts)>0:
            st.subheader(pdgb.loc[i,'Sedes'])
            for al in alerts:
                st.write(al.text)
        else:
            st.subheader(pdgb.loc[i,'Sedes'])
            st.write("sin NOTAM, puede volar tranquilo.")
        wdec('#esri_dijit_Search_0 > div > div.searchExpandContainer > div > div.searchInputGroup > div.searchClear > span.searchIcon.esri-icon-close.searchClose').click()
    driver.quit()
