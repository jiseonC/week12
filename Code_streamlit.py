# 1. Import Library
import streamlit as st

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
	
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd  
import time

# 2. recruit web page crawling methods
def jk_recruit_info(url = 'https://www.jobkorea.co.kr/Search/?stext=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D'):
    # Service, Driver
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    # 페이지 로드를 위해 초 대기
    wait = WebDriverWait(driver, 10) 

    job_table = driver.find_elements(By.CSS_SELECTOR, '#dev-content-wrap > article > section.content-recruit.on > article.list > article')

    job_info = []

    for job in job_table:
        company_name = job.find_element(By.CLASS_NAME, 'corp-name-link.dev-view').text
        job_desc = job.find_element(By.CLASS_NAME, 'information-title-link.dev-view').text
        job_desc_detail = job.find_element(By.CLASS_NAME, 'chip-information-group').text.split('\n')
        job_url = job.find_element(By.CLASS_NAME, 'information-title-link.dev-view').get_attribute("href")
        
        job_info.append({'Site':'Job_Korea', 'Col_Company':company_name, 'Col_Recruit':job_desc, 'Col_detail':job_desc_detail, 'Col_url':job_url})
        
    driver.quit()

    jk_df = pd.DataFrame(job_info)

    return jk_df
    
def si_recruit_info(url='https://www.saramin.co.kr/zf_user/search?searchword=%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n'):
    # Service, Driver
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    # 페이지 로드를 위해 초 대기
    wait = WebDriverWait(driver, 10) 

    job_table = driver.find_element(By.XPATH, '//*[@id="recruit_info_list"]/div[1]')
    job_lists = driver.find_elements(By.CLASS_NAME, 'item_recruit')

    job_info = []

    for job in job_lists:
        company_name = job.find_element(By.CLASS_NAME, 'corp_name').text 
        job_desc = job.find_element(By.CSS_SELECTOR, 'h2').text
        job_desc_detail = job.find_element(By.CLASS_NAME, 'job_condition').text.split('\n')
        job_url = job.find_element(By.CSS_SELECTOR, 'h2 > a').get_attribute('href')

        job_info.append({'Site':'Saramin', 'Col_Company':company_name, 'Col_Recruit':job_desc, 'Col_detail':job_desc_detail, 'Col_url':job_url})
        
    driver.quit()

    si_df = pd.DataFrame(job_info)

    return si_df

def all_recruit_info() : 
    jk_df = jk_recruit_info()
    si_df = si_recruit_info()

    return jk_df, si_df

def concat_recruit_df(df1, df2):
    concat_df = pd.concat([df1, df2]).reset_index(drop=True)
    return concat_df

def ratio_df(df):
    df = df['Site'].value_counts().reset_index().rename(columns={'count':'Count'})
    df['Ratio'] = round((df['Count'] / df['Count'].sum())*100, 2)
    return df
    
def visualize_df(df):
    fig = px.pie(df, names=df['Site'], values=df['Ratio'], title='Recruitment Ratio')
    return fig


st.title('Title')

# 
with st.form('form'): 
    submit_button1 = st.form_submit_button('Recruit Searching')

    if submit_button1:
        df1, df2 = all_recruit_info()
        df3 = concat_recruit_df(df1, df2)
        df4 = ratio_df(df3)
        df5 = visualize_df(df4)

        st.write(df3)
        st.write(df4)   
        st.write(df5)