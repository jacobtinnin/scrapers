# -*- coding: utf-8 -*-
"""
Created on Tue Jan 07 15:41:12 2020

@author: Jacob
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

for year in range(2013,2014,1):
    def getSchools():
        url = "https://www.sports-reference.com/cbb/seasons/"+str(year)+"-ratings.html"
        page = urlopen(url).read()
        soup = BeautifulSoup(page,features="lxml")
        table = soup.find("tbody")
        school_dict = dict()
        for row in table.findAll('td', {"data-stat": "school_name"}):
            school_name = row.getText()
            for a in row.find_all('a', href=True):
                link = a['href'].strip()
                name = link[13:].split("/")[0]
                school_dict[name] = school_name
                
        return school_dict
    def getDfs():
        school_set = getSchools()
        final_df=pd.DataFrame()
        for school in school_set: 
            url = "https://www.sports-reference.com/cbb/schools/" + school + "/"+str(year)+"-schedule.html"
            page = urlopen(url).read()
            soup = BeautifulSoup(page,features="lxml")
            pre_df = dict()
            table = soup.findAll("tbody")
            table = table[-1]
            featuresWanted =  {'date_game','game_location','opp_name',
                               'pts','opp_pts'} #add more features here!!
            rows = table.find_all('tr')
            for row in rows:
                if (row.find('th', {"scope":"row"}) != None):
                    for f in featuresWanted:
                        cell = row.find("td",{"data-stat": f})
                        a = cell.text.strip().encode()
                        text=a.decode("utf-8")
                        if f in pre_df:
                            pre_df[f].append(text)
                        else:
                            pre_df[f]=[text]
                
            df = pd.DataFrame.from_dict(pre_df)
            df['opp_name']= df['opp_name'].apply(lambda row: (row.split("\xa0(")[0]).rstrip())
            df["school_name"]=school_set[school]
            df["school_name"] = df["school_name"].apply(removeNCAA)
            final_df=pd.concat([final_df,df])
        return final_df
    
    def removeNCAA(x):
        if("NCAA" in x):
            return x[:-5]
        else:
            return x
    
    def csvDump():
        df=getDfs()
        df.to_csv("scraped_elo_data_"+str(year)+".csv")
    csvDump()