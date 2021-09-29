#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 11:21:08 2021

@author: nuoyuan
"""

import requests
import json
from requests_oauthlib import OAuth1Session
import time

global consumer_key
global cnsumer_secret
global access_token
global access_secret
consumer_key="1diOSALtPxLkU91JA9AGRs8Hd"
consumer_secret="yOyxkQEQtp2rA7qMA4uVqA3HISzDuj7zKtQqEBT1l3r8kXt5V3"
access_token="1396657611575947264-rnwSHbYqL2WKLkFZRK5xS4dF8L9o51"
access_secret="qkQ6mPtyPrQIxOdI5gB6DkVX6pRQ1jxn2XQaodXrl5qki"

def create_headers(consumer_key,nonce,signature_method,token,api_version,consumer_secret,token_secret):
    return {"oauth_consumer_key":consumer_key,
            "oauth_nonce":nonce,
            "oauth_signaure_method":signature_method,
            "oauth_timestamp":time.time(),
            "oauth_token":token,
            "oauth_version":api_version,
            "consumer_secret":consumer_secret,
            "oauth_token_secret":token_secret
            }


def get_params(list_id,count,include_entities,skip_status):
    return {"list_id":str(list_id),
            "count":str(count),
            "include_entities":include_entities,
            "skip_status":skip_status}
    

def create_oauth1_session():
    return OAuth1Session(consumer_key,consumer_secret,access_token,access_secret)



def connect_to_endpoint(resource_url,params):
    oauth1=create_oauth1_session()
    json_response=oauth1.get(resource_url,params=params)
    if json_response.status_code != 200:
        print("[Error] Twitter API HTTP Reponse Error:"+str(json_response.status_code))
    content=json.loads(json_response.text)
    return content

def main():
    resource_url="https://api.twitter.com/1.1/lists/members.json"
    list_id=34179516
    count=5000
    include_entities=False
    skip_status=True
    params=get_params(list_id,count,include_entities,skip_status)
    content=connect_to_endpoint(resource_url,params)
    members=content["users"]
    with open("Handle_ids.txt","a+") as f:
        for member in members:
            f.write(member["screen_name"]+"|"+member["name"]+"|"+member["id_str"]+"\n")
            
    
    
if __name__=="__main__":
    main()
    