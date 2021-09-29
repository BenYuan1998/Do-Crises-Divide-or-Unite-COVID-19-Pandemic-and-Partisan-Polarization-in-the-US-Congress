#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 18:10:14 2021

@author: nuoyuan
"""
import csv

path_pre="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_pre_covid_retweets_removed.csv"
path_during="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_during_covid_retweets_removed.csv"

dict_hashtags_pre=dict()
dict_hashtags_during=dict()

with open(path_pre,"r+") as f:
    reader=csv.reader(f)
    for line in reader:
        hashtags=line[7]
        if (hashtags!="Hashtags") and (hashtags!="None"):
            for hashtag in eval(hashtags):
                hashtag=hashtag.lower()
                dict_hashtags_pre[hashtag]=dict_hashtags_pre.get(hashtag,0)+1
                
with open(path_during,"r+") as f:
    reader=csv.reader(f)
    for line in reader:
        hashtags=line[7]
        if (hashtags!="Hashtags") and (hashtags!="None"):
            for hashtag in eval(hashtags):
                hashtag=hashtag.lower()
                dict_hashtags_during[hashtag]=dict_hashtags_during.get(hashtag,0)+1


hashtag_frequency_pairs_pre_descending=sorted(list(dict_hashtags_pre.items()),key=lambda x:x[1],reverse=True)
hashtag_frequency_pairs_during_descending=sorted(list(dict_hashtags_during.items()),key=lambda x:x[1],reverse=True)


print(len(hashtag_frequency_pairs_pre_descending),"\n",len(hashtag_frequency_pairs_during_descending))
print(hashtag_frequency_pairs_pre_descending[:10])
print(hashtag_frequency_pairs_during_descending[:10])





