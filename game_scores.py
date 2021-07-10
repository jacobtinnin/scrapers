# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:34:33 2021

@author: Jacob
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

final_df=pd.DataFrame()
count=0;
for month in ('december','january','february','march','april','may'):
    url = "https://www.basketball-reference.com/leagues/NBA_2021_games-" + month + ".html"
    page = urlopen(url).read()
    soup = BeautifulSoup(page,features="lxml")
    table = soup.find("tbody")
    game_dict = dict()
    for row in table.findAll('td', {"data-stat": "box_score_text"}):
        for a in row.find_all('a', href=True):
            link = a['href'].strip()
            date = link.split("/")[2]
            date = date[0:8]
            game_dict[link] = date
    for game in game_dict: 
        count=count+1;
        url = "https://www.basketball-reference.com/" + game
        page = urlopen(url).read()
        soup = BeautifulSoup(page,features="lxml")
        pre_df = dict()
        tables = soup.findAll("tbody")
        featuresWanted =  {'mp','bpm'} #add more features here!!
        for i in range(len(tables)):
            table = tables[i]
            if len(table.findAll('td', {"data-stat": "bpm"})) > 0:
                rows = table.find_all('tr')
                for row in rows:
                    if (row.find('td', {"data-stat": "bpm"}) != None):
                        cell = row.find("th",{"data-stat": 'player'})
                        a = cell.text.strip().encode()
                        text=a.decode("utf-8")
                        if 'player' in pre_df:
                            pre_df['player'].append(text)
                        else:
                            pre_df['player']=[text]
                            
                        for f in featuresWanted:
                            cell = row.find("td",{"data-stat": f})
                            a = cell.text.strip().encode()
                            text=a.decode("utf-8")
                            if f in pre_df:
                                pre_df[f].append(text)
                            else:
                                pre_df[f]=[text]
                
        df = pd.DataFrame.from_dict(pre_df)
        df["date"]=game_dict[game]
        df["game_id"]=count;
        final_df=pd.concat([final_df,df])

final_df.to_csv("2021_games.csv")