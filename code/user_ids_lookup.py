#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 17:15:32 2021

@author: nuoyuan
"""
import requests
import json

def get_params(usernames): # usernames is a comma-separated string of Twitter usernames. For example, usernames="Twitter,TwitterDev".
    return {"usernames":usernames}

def create_headers(bearer_token):
    headers={"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url,headers,params):
    response=requests.request("GET",url,headers=headers,params=params)
    if response.status_code!=200:
        raise Exception("Request returned an error:{} {}".format(response.status_code,response.text))
    return response.json()

def main():
    url="https://api.twitter.com/2/users/by"
    bearer_token="AAAAAAAAAAAAAAAAAAAAAJZLQAEAAAAAmCdQ8%2BlUTcasTvpQjMOqPTmFH9o%3D1c3awro6E9Ll7XfZAoth2SmSNdRDziA1RgTVUmydudfUTKz4td"
    headers=create_headers(bearer_token)
    usernames="SenMurphyOffice"
    params=get_params(usernames)
    json_response=connect_to_endpoint(url,headers=headers,params=params)
    print(json_response)
    #print(type(json.dumps(json_response,indent=4,sort_keys=True)))
    #user_ids=json_response["data"]
    #with open("User_ids.txt","a+") as f:
        #for user_id in user_ids:
            #f.write(user_id["name"]+"|"+user_id["username"]+"|"+user_id["id"]+"\n")
       
    
if __name__=="__main__":
    main()
    
    
