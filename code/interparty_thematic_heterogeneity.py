#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 18:50:20 2021

@author: nuoyuan
"""
import csv
import pandas as pd
import numpy as np
#from sklearn.model_selection import StratifiedKFold
import tqdm
import pytz
import datetime


"""
This script is the collection of functions that together compute the Weighted Squared Difference in Importance Ratio (WSDIR)
of a corpus composed of documents belonging to one of the two groups.
"""

# Specify the filepaths for the pre-COVID corpus and the during-COVID corpus.
path_pre="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_pre_covid_retweets_removed.csv"
path_during="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_during_covid_retweets_removed.csv"

def extract_docs_with_hashtags(filepath):
    df=pd.read_csv(filepath,header=0)
    df_hashtags=df[df["Hashtags"]!="None"]
    df_hashtags["Hashtags"]=df_hashtags["Hashtags"].map(lambda x:eval(x)) # Use eval to convert string back to set.
    return df_hashtags

def duplicate_docs(df):
    columns=list(df.columns)
    data_duplicated=list()
    data=df.values.tolist() # Convert df to a list (note that this operation leaves out the column labels).
    for line in data:
        hashtags=line[-1]
        for hashtag in hashtags:
            new_line=line
            del new_line[-1]
            new_line.append(hashtag)
            data_duplicated.append(new_line)
    df_duplicated=pd.DataFrame(data_duplicated,columns=columns)
    return df_duplicated


def top_K_hashtags(df_Dem,df_Rep,K):
    # This function gives two lists of top-K hashtags most discussed by Democratic members and Republican members respectively.
    results_Dem={"hashtag_Democratic":[]}
    results_Rep={"hashtag_Republican":[]}
    hashtag_frequency_pairs_Dem=dict()
    hashtag_frequency_pairs_Rep=dict()
    for hashtag in df_Dem["Hashtags"].tolist():
        hashtag_frequency_pairs_Dem[hashtag]=hashtag_frequency_pairs_Dem.get(hashtag,0)+1
    for hashtag in df_Rep["Hashtags"].tolist():
        hashtag_frequency_pairs_Rep[hashtag]=hashtag_frequency_pairs_Rep.get(hashtag,0)+1
    for hashtag in hashtag_frequency_pairs_Dem.keys():
        hashtag_frequency_pairs_Dem[hashtag]=hashtag_frequency_pairs_Dem[hashtag]/sum(hashtag_frequency_pairs_Dem.values())
    for hashtag in hashtag_frequency_pairs_Rep.keys():
        hashtag_frequency_pairs_Rep[hashtag]=hashtag_frequency_pairs_Rep[hashtag]/sum(hashtag_frequency_pairs_Rep.values())
    hashtag_frequency_pairs_Dem=list(hashtag_frequency_pairs_Dem.items())
    hashtag_frequency_pairs_Rep=list(hashtag_frequency_pairs_Rep.items())
    hashtag_frequency_pairs_Dem=sorted(hashtag_frequency_pairs_Dem,key=lambda x:x[1],reverse=True)
    hashtag_frequency_pairs_Rep=sorted(hashtag_frequency_pairs_Rep,key=lambda x:x[1],reverse=True)
    for hashtag_frequency_pair in hashtag_frequency_pairs_Dem[:K]:
        results_Dem["hashtag_Democratic"].append(hashtag_frequency_pair)
    for hashtag_frequency_pair in hashtag_frequency_pairs_Rep[:K]:
        results_Rep["hashtag_Republican"].append(hashtag_frequency_pair)
    index=list(range(1,K+1,1))
    results_Dem=pd.DataFrame(results_Dem,index=index)
    results_Rep=pd.DataFrame(results_Rep,index=index)
    results=pd.concat([results_Dem,results_Rep],axis=1)
    return results
    
        

def compute_WSDIR(df):
    # First, we identify all the unique hashtags contained in df and calculate their frequencies.
    # The results are stored in a dictionary with keys being the hashtags and values being their
    # respective frequencies.
    hashtag_frequency_pairs=dict()
    for hashtag in df["Hashtags"].tolist():
        hashtag_frequency_pairs[hashtag]=hashtag_frequency_pairs.get(hashtag,0)+1
    tweets_Dem=df[df["party_affiliation"]=="Democratic"]
    tweets_Rep=df[df["party_affiliation"]=="Republican"]
    num_tweets_Dem=tweets_Dem.shape[0]
    num_tweets_Rep=tweets_Rep.shape[0]
    total_num_tweets=num_tweets_Dem+num_tweets_Rep
    IRs_Dem=list()
    IRs_Rep=list()
    weights_hashtags=list()
    for target_hashtag,frequency in hashtag_frequency_pairs.items():
        num_tweets_Dem_hashtag=0
        num_tweets_Rep_hashtag=0
        for hashtag in tweets_Dem["Hashtags"]:
            if target_hashtag==hashtag:
                num_tweets_Dem_hashtag+=1
        for hashtag in tweets_Rep["Hashtags"]:
            if target_hashtag==hashtag:
                num_tweets_Rep_hashtag+=1
        IR_Dem=num_tweets_Dem_hashtag/num_tweets_Dem
        IR_Rep=num_tweets_Rep_hashtag/num_tweets_Rep
        weight_hashtag=frequency/total_num_tweets
        IRs_Dem.append(IR_Dem)
        IRs_Rep.append(IR_Rep)
        weights_hashtags.append(weight_hashtag)
    SDIRs=list()
    num_hashtags=len(hashtag_frequency_pairs.keys())
    for index in range(num_hashtags):
        SDIR=(IRs_Dem[index]-IRs_Rep[index])**2
        SDIRs.append(SDIR)
    WSDIR=0
    for index in range(num_hashtags):
        WSDIR+=SDIRs[index]*weights_hashtags[index]
    return WSDIR

def est_to_utc(date_string): # Format of date_string: "YYYY-mm-dd HH:MM:SS". Moreover, date_string should be a string.
    local_time=pytz.timezone("US/Eastern")
    naive_datetime=datetime.datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S")
    local_datetime=local_time.localize(naive_datetime,is_dst=None)
    utc_datetime=local_datetime.astimezone(pytz.utc)
    return utc_datetime

def utc_in_iso(utc_datetime):
    return str(utc_datetime.isoformat()).replace("+00:00","Z")

def str_to_pandas_timestamp(sub_intervals):
    results=list()
    for sub_interval in sub_intervals:
        start,end=sub_interval[0],sub_interval[1]
        start,end=est_to_utc(start),est_to_utc(end)
        start,end=utc_in_iso(start),utc_in_iso(end)
        start,end=pd.to_datetime(start),pd.to_datetime(end)
        results.append((start,end))
    return results
         
def experiment(sub_intervals,df):
    # Note: For sub_intervals, it should be formatted as a list of tuples. 
    #For each tuple, its first entry is the moment when a sub-interval starts and its second entry is the moment when the interval ends.
    results={"Sample":[],
             "WSDIR":[],
             }
    df["created_at"]=pd.to_datetime(df["created_at"])
    sample_name=1
    pbar=tqdm.tqdm(total=len(sub_intervals))
    for sub_interval in sub_intervals:
        sample=df.loc[(df["created_at"]>=sub_interval[0]) & (df["created_at"]<=sub_interval[1])]
        WSDIR=compute_WSDIR(sample)
        if sample_name==1:
            results["Sample"].append(f"{sample_name}st sample")
        elif sample_name==2:
            results["Sample"].append(f"{sample_name}nd sample")
        elif sample_name==3:
            results["Sample"].append(f"{sample_name}rd sample")
        else:
            results["Sample"].append(f"{sample_name}th sample")
        results["WSDIR"].append(WSDIR)
        sample_name+=1
        pbar.update(1)
    pbar.close()
    results=pd.DataFrame(results)
    return results


def main():
    sub_intervals_pre=[("2019-11-17 00:00:00","2019-11-23 23:59:59"),
                       ("2019-11-24 00:00:00","2019-11-29 23:59:59"),
                       ("2019-11-30 00:00:00","2019-12-05 23:59:59"),
                       ("2019-12-06 00:00:00","2019-12-11 23:59:59"),
                       ("2019-12-12 00:00:00","2019-12-17 23:59:59"),
                       ("2019-12-18 00:00:00","2019-12-23 23:59:59"),
                       ("2019-12-24 00:00:00","2019-12-29 23:59:59"),
                       ("2019-12-30 00:00:00","2020-01-04 23:59:59"),
                       ("2020-01-05 00:00:00","2020-01-10 23:59:59"),
                       ("2020-01-11 00:00:00","2020-01-17 23:59:59")]
    sub_intervals_during=[("2020-03-13 00:00:00","2020-03-19 23:59:59"),
                          ("2020-03-20 00:00:00","2020-03-25 23:59:59"),
                          ("2020-03-26 00:00:00","2020-03-31 23:59:59"),
                          ("2020-04-01 00:00:00","2020-04-06 23:59:59"),
                          ("2020-04-07 00:00:00","2020-04-12 23:59:59"),
                          ("2020-04-13 00:00:00","2020-04-18 23:59:59"),
                          ("2020-04-19 00:00:00","2020-04-24 23:59:59"),
                          ("2020-04-25 00:00:00","2020-04-30 23:59:59"),
                          ("2020-05-01 00:00:00","2020-05-06 23:59:59"),
                          ("2020-05-07 00:00:00","2020-05-13 23:59:59")]
    sub_intervals_pre=str_to_pandas_timestamp(sub_intervals_pre)
    sub_intervals_during=str_to_pandas_timestamp(sub_intervals_during)
    df_pre_hashtags=extract_docs_with_hashtags(path_pre)
    df_during_hashtags=extract_docs_with_hashtags(path_during)
    df_pre_hashtags_expanded=duplicate_docs(df_pre_hashtags)
    df_during_hashtags_expanded=duplicate_docs(df_during_hashtags)
    results_pre=experiment(sub_intervals_pre,df_pre_hashtags_expanded)
    results_during=experiment(sub_intervals_during,df_during_hashtags_expanded)
    return results_pre,results_during
    
if __name__=="__main__":
    K=10
    df_pre=extract_docs_with_hashtags(path_pre)
    df_pre=duplicate_docs(df_pre)
    df_Dem_pre=df_pre[df_pre["party_affiliation"]=="Democratic"]
    df_Rep_pre=df_pre[df_pre["party_affiliation"]=="Republican"]
    top_K_hashtags_pre=top_K_hashtags(df_Dem_pre,df_Rep_pre,K)
    df_during=extract_docs_with_hashtags(path_during)
    df_during=duplicate_docs(df_during)
    df_Dem_during=df_during[df_during["party_affiliation"]=="Democratic"]
    df_Rep_during=df_during[df_during["party_affiliation"]=="Republican"]
    top_K_hashtags_during=top_K_hashtags(df_Dem_during, df_Rep_during,K)
    #results_pre,results_during=main()

    
