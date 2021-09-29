#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 16:17:35 2021

@author: nuoyuan
"""

import requests
import json
import pandas as pd


def create_headers(bearer_token):
    headers={"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url,headers):
    response=requests.request("GET",url,headers=headers)
    if response.status_code!=200:
        raise Exception("Request returned an error:{} {}".format(response.status_code,response.text))
    return response.json()

def id_extractor(file_path):
    df=pd.read_csv(file_path,header=0)
    return df["Uid"].values.tolist() # The output is a list object.
        
    
def main():
    url="https://api.twitter.com/2/users/"
    bearer_token="AAAAAAAAAAAAAAAAAAAAAJZLQAEAAAAAmCdQ8%2BlUTcasTvpQjMOqPTmFH9o%3D1c3awro6E9Ll7XfZAoth2SmSNdRDziA1RgTVUmydudfUTKz4td"
    headers=create_headers(bearer_token)
    path_senate="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/Data/congress116_senate_accounts.csv"
    path_house="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/Data/congress116_house_accounts.csv"
    ids_senate=id_extractor(path_senate)
    ids_house=id_extractor(path_house)
    ids_congress=ids_senate+ids_house
    f=open("116th_Congress_twitter_handles.txt","a+")
    for handle_id in ids_congress:
        handle_url=url+(str(handle_id))
        data=connect_to_endpoint(url=handle_url,headers=headers)
        if "errors" not in data.keys(): # Check whether there is a Twitter account associated with a given handle id. 
           f.write(data["data"]["id"]+"|"+data["data"]["name"]+"|"+data["data"]["username"]+"\n") 
    f.close()
       

if __name__=="__main__":
    main()