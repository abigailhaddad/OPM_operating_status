# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 09:47:05 2018
This pulls from the USAJOBS operating status API and outputs a spreadsheet with historical data
@author: abhaddad
"""
import pandas as pd
from bs4 import BeautifulSoup 
import requests
import os

def get_operating_status_by_date(date):
    url=f'https://www.opm.gov/xml/operatingstatus.xml?date={date}&markup=on'
    response = requests.get(url)
    # Extracting the source code of the page.
    data = response.text
    # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data, 'xml')
    Status=soup.find('OperatingStatus').text
    #ShortStatusMessage=soup.find('ShortStatusMessage').text
    return(date, Status)

def get_operating_status_by_date_range(begin_date, end_date):
    datelist = pd.date_range(pd.to_datetime(begin_date), pd.to_datetime(end_date)).tolist()
    df = pd.DataFrame()
    for date in datelist:
        string_date=date.strftime("%D")
        date, Status=(get_operating_status_by_date(string_date))
        df=df.append({'Date': date, 'Status': Status}, ignore_index=True)
    return(df)

def output_file(directory, begin_date, end_date):
    df=get_operating_status_by_date_range(begin_date, end_date)
    os.chdir(directory)
    name_of_file=f'Operating_Status{begin_date.replace("/","")}_to{end_date.replace("/","")}.xlsx'
    df.to_excel(name_of_file)
    
begin_date="05/01/2018"
end_date="07/25/2018"
directory=r"C:\Users\abhaddad\Documents\Learning More Python\API pull"

output_file(directory, begin_date, end_date)

