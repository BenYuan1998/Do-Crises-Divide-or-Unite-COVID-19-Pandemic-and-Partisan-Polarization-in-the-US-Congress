#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:48:43 2021

@author: nuoyuan
"""

import re
import pandas as pd
import csv


def detect_hashtags(document):
    pattern=r'\B#\w*[a-zA-Z]+\w*'
    re_object=re.compile(pattern)
    results=re_object.findall(document)
    if len(results)==0: # Check whether there is any successful match. 
        return "None"
    else:
        return set(results)

# Extract the hashtags from each tweet contained in the pre-COVID coprus and the during-COVID corpus.
path_pre="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_pre_covid_retweets_removed.csv"
path_during="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_during_covid_retweets_removed.csv"
hashtags_pre=list()
hashtags_during=list()
with open(path_pre,"r+") as f:
    reader=csv.reader(f)
    for index,line in enumerate(reader):
        if index!=0:
            tweet=line[4]
            hashtags=detect_hashtags(tweet)
            hashtags_pre.append(hashtags)
with open(path_during,"r+") as f:
    reader=csv.reader(f)
    for index,line in enumerate(reader):
        if index!=0:
            tweet=line[4]
            hashtags=detect_hashtags(tweet)
            hashtags_during.append(hashtags)

# Add hashtags_pre to the pre-COVID corpus and hashtags_during to the during-COVID corpus as two new columns.
df_pre=pd.read_csv(path_pre,header=0)
df_during=pd.read_csv(path_during,header=0)
df_pre.drop(columns="Hashtags")
df_during.drop(columns="Hashtags")
df_pre["Hashtags"]=hashtags_pre
df_during["Hashtags"]=hashtags_during
df_pre.to_csv(path_pre,index=False)
df_during.to_csv(path_during,index=False)

        





