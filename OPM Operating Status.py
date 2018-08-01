# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 09:47:05 2018
This pulls from the USAJOBS operating status API and outputs a spreadsheet with historical data.
@author: abhaddad
"""
#This imports all of the packages you'll need
import pandas as pd
from bs4 import BeautifulSoup 
import requests
import os


def get_operating_status_by_date(date, JSON=True):
    #Pulling from the XML API
    if JSON==False:
        """
        This functions defaults to pulling from the JSON API, but FYI this is how you
        pull from the XML API. (They have the same information.)
        The disadvantage of the XML API that there's an extra step: you have
        to parse the result of your requests query using BeautifulSoup, just
        like you would have to parse the html if you were scraping a website
        """
        #the url is an f-string: the {date} field pulls in your date argument
        url=f'https://www.opm.gov/xml/operatingstatus.xml?date={date}&markup=on'
        #this is where you use the requests library to pull from the url
        response = requests.get(url)
        #we now get the text of that output
        data = response.text
        #and because we pulled from the XML API, we now parse it with Beautiful Soup
        soup = BeautifulSoup(data, 'xml')
        #we're now looking for the OperatingStatus tag and getting the text next to it
        Status=soup.find('OperatingStatus').text
    #Pulling from the JSON API 
    if JSON==True:
        """
        With the JSON, we read the output right into a dictionary file.
        """
        url=f"https://www.opm.gov/xml/operatingstatus.json?date={date}&markup=on"
        response = requests.get(url)
        cont = response.json()
        Status=cont['StatusSummary']
    return(date, Status)


def get_operating_status_by_date_range(begin_date, end_date):
    #this takes the begin_date and end_date, converts both to a date format, and generates a list of all the dates in between
    datelist = pd.date_range(pd.to_datetime(begin_date), pd.to_datetime(end_date)).tolist()
    #this creates a blank data frame
    df = pd.DataFrame()
    #this populates the data frame with dates and status
    for date in datelist:
        #this formats the date the way we want it for the API URLS
        string_date=date.strftime("%D")
        #this refers to the earlier function which does the actual requests
        date, Status=(get_operating_status_by_date(string_date))
        #this puts the output of that function in our data frame
        df=df.append({'Date': date, 'Status': Status}, ignore_index=True)
    return(df)

def output_file(directory, begin_date, end_date):
    #this calls the function which generates the data drame of dates/statuses
    df=get_operating_status_by_date_range(begin_date, end_date)
    #this changes your directory
    os.chdir(directory)
    #this names the file based on the beginning and end-date
    #note again the f-string; here, we're modifying the begin_date and end_date fields to take out slashes
    name_of_file=f'Operating_Status{begin_date.replace("/","")}_to{end_date.replace("/","")}.xlsx'
    #this outputs the data frame to an excel file
    df.to_excel(name_of_file)
    return(df)

#here I'm defining my variables
begin_date="07/01/2018"
end_date="07/25/2018"
#this is a raw string because I have spaces in my directory
directory=r"C:\Users\abhaddad\Documents\Learning More Python\API pull"

#here I'm calling the function; this also gives me the df to play with
df=output_file(directory, begin_date, end_date)
