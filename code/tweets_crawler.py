#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:34:10 2021

@author: nuoyuan
"""

import requests
import os
import json
import pytz
import datetime
from datetime import timezone
#from ratelimit import limits,sleep_and_retry
import time
import csv



def date_range(start, end, intv):
    from datetime import datetime
    start = datetime.strptime(start,"%Y-%m-%d")
    end = datetime.strptime(end,"%Y-%m-%d")
    diff = (end  - start ) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y-%m-%d")
    yield end.strftime("%Y-%m-%d")
    

def est_to_utc(date_string): # Format of date_string: "YYYY-mm-dd HH:MM:SS". Moreover, date_string should be a string.
    local_time=pytz.timezone("US/Eastern")
    naive_datetime=datetime.datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S")
    local_datetime=local_time.localize(naive_datetime,is_dst=None)
    utc_datetime=local_datetime.astimezone(pytz.utc)
    return utc_datetime

def utc_in_iso(utc_datetime):
    return str(utc_datetime.isoformat()).replace("+00:00","Z")
     
def get_params(query,start_time,end_time,next_token_exist,next_token=None):
    #return {"max_results":100}
    if next_token_exist==False:
        return {"query":query, # To retrieve all the English tweets posted by account SenMurphyOffice (account id: 2853793517) 
                       # the proper string query should look the following: from:SenMurphyOffice lang:en.    
                "start_time":start_time,
                "end_time":end_time,
                "max_results":100,
                "tweet.fields":"created_at,id,text,author_id"}
    else:
        return {"query":query, # To retrieve all the English tweets posted by account SenMurphyOffice (account id: 2853793517) 
                       # the proper string query should look the following: from:SenMurphyOffice lang:en.    
                "start_time":start_time,
                "end_time":end_time,
                "max_results":100,
                "next_token":next_token,
                "tweet.fields":"created_at,id,text,author_id"}
        

def create_headers(bearer_token):
    headers={"Authorization": "Bearer {}".format(bearer_token)}
    return headers



def connect_to_endpoint(url,headers,params):
    response=requests.request("GET",url,headers=headers,params=params)
    if (response.status_code!=200) and (response.status_code!=429):
        raise Exception("Request returned a non-rate-limit error:{} {}".format(response.status_code,response.text))
    elif response.status_code==429:
        raise Exception("The rate limit will reset in {} seconds after the unix epoch.".format(float(response.header["x-rate-limit-reset"])))
    else:
        return response.json()

 
def main():
    url="https://api.twitter.com/2/tweets/search/all"
    bearer_token="AAAAAAAAAAAAAAAAAAAAAJZLQAEAAAAAmCdQ8%2BlUTcasTvpQjMOqPTmFH9o%3D1c3awro6E9Ll7XfZAoth2SmSNdRDziA1RgTVUmydudfUTKz4td"
    headers=create_headers(bearer_token)
    start_time="2019-11-17 00:00:00" # Specify the start time of the data collection window.
    end_time="2020-01-17 23:59:59" # Specify the end time of the data collection window.
    start_utc=est_to_utc(start_time)
    end_utc=est_to_utc(end_time)
    start_utc_iso=utc_in_iso(start_utc)
    end_utc_iso=utc_in_iso(end_utc)
    twitter_handle_path="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/Data/116th_Congress_twitter_handles_final.txt"
    f=open(twitter_handle_path,"r")
    #base_path="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/Data/Members_tweets_during_COVID_19"
    #base_path="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/Data/Members_tweets_pre_COVID_19"
    header=["username","account_id","member","party_affiliation","tweet_text","created_at","tweet_id"]
    with open("tweets_pre_covid_final.csv","a+",encoding="utf-8",newline="") as g:
        csvg=csv.writer(g)
        #csvg.writerow(header)
        for line in f.readlines()[651:]:
            party,account_id,name,username,member=line.split("|")
            member=member.replace("\n","")
            query="from:"+account_id+" "+"lang:en" # Construct the string query for a specific Twitter account using its numeric account id.
            meta={"next_token":0}
            while "next_token" in meta.keys(): # This condition checks whether there are additional pages of data.
                if meta["next_token"]==0:# This condition checks whether it is the first query for a given Twitter account.
                    next_token_exist=False
                    params=get_params(query,start_utc_iso,end_utc_iso,next_token_exist)
                    json_response=connect_to_endpoint(url,headers,params)
                    if json_response["meta"]["result_count"]!=0: # If no tweets were matched during the first query, move on to the next Twitter account in line.
                        data=json_response["data"]
                        meta=json_response["meta"]
                        for tweet in data:
                            data=(username,account_id,member,party,tweet["text"],tweet["created_at"],tweet["id"])
                            csvg.writerow(data)
                    else:
                        break
                else:
                    next_token_exist=True
                    next_token=meta["next_token"]
                    params=get_params(query,start_utc_iso,end_utc_iso,next_token_exist,next_token)
                    json_response=connect_to_endpoint(url,headers,params)
                    if json_response["meta"]["result_count"]!=0:
                        data=json_response["data"]
                        meta=json_response["meta"]
                        for tweet in data:
                            data=(username,account_id,member,party,tweet["text"],tweet["created_at"],tweet["id"])
                            csvg.writerow(data)
                    else:
                        break
                time.sleep(4) # To prevent sending API requests at a rate exceeding the 300 requests/15 minutes rate limit.
    f.close()                
if __name__=="__main__":
    main()
    
    
    
    
    
    