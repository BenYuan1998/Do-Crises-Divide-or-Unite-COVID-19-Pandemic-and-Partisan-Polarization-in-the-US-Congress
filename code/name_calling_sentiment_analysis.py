#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 12:03:58 2021

@author: nuoyuan
"""

import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from data_cleaning import remove_links,remove_non_ascii,lower_case



# Load the pre-COVID and during-COVID corpora. 



path_pre="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_pre_covid_retweets_removed.csv"
path_during="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_during_covid_retweets_removed.csv"
df_pre=pd.read_csv(path_pre,header=0)
df_during=pd.read_csv(path_during,header=0)

# Select all the Democratic-authored tweets from the pre-COVID and during-COVID corpora.
Dem_tweets_pre=df_pre[df_pre["party_affiliation"]=="Democratic"]["tweet_text"]
Dem_tweets_during=df_during[df_during["party_affiliation"]=="Democratic"]["tweet_text"]

# Select all the Democratic-authored tweets that explicitly mentioned the Trump Administration via a dictionary-based method.
dictionary=["trump","president","white house","whitehouse","executive branch","executivebranch"] 
results_pre={"Tweet":list(),
             "Keywords_in_tweet":list(),
             "Positive_valence":list(),
             "Neutral_valence":list(),
             "Negative_valence":list(),
             "Compound_sentiment_intensity":list()}
results_during={"Tweet":list(),
             "Keywords_in_tweet":list(),
             "Positive_valence":list(),
             "Neutral_valence":list(),
             "Negative_valence":list(),
             "Compound_sentiment_intensity":list()}
# Create a sentiment intensity analyzer object based on the vader lexicon pretrained for social media content.
sia=SentimentIntensityAnalyzer()
for tweet in Dem_tweets_pre:
    # Preprocess the tweet by removing all the links and non-ascii characters and lowercase the tweet.
    tweet=remove_links(tweet)
    tweet=remove_non_ascii(tweet)
    tweet=lower_case(tweet)
    if any(keyword in tweet for keyword in dictionary)==True:
        keywords_in_tweet=list()
        for keyword in dictionary:
            if keyword in tweet:
                keywords_in_tweet.append(keyword)
        results_pre["Keywords_in_tweet"].append(keywords_in_tweet)
        results_pre["Tweet"].append(tweet)
        # Compute the sentiment intensity scores of the tweet.
        sent_intensity_scores=sia.polarity_scores(tweet)
        results_pre["Positive_valence"].append(sent_intensity_scores["pos"])
        results_pre["Neutral_valence"].append(sent_intensity_scores["neu"])
        results_pre["Negative_valence"].append(sent_intensity_scores["neg"])
        results_pre["Compound_sentiment_intensity"].append(sent_intensity_scores["compound"])
for tweet in Dem_tweets_during:
    # Preprocess the tweet by removing all the links and non-ascii characters and lowercase the tweet.
    tweet=remove_links(tweet)
    tweet=remove_non_ascii(tweet)
    tweet=lower_case(tweet)
    if any(keyword in tweet for keyword in dictionary)==True:
        keywords_in_tweet=list()
        for keyword in dictionary:
            if keyword in tweet:
                keywords_in_tweet.append(keyword)
        results_during["Keywords_in_tweet"].append(keywords_in_tweet)
        results_during["Tweet"].append(tweet)
        # Compute the sentiment intensity scores of the tweet.
        sent_intensity_scores=sia.polarity_scores(tweet)
        results_during["Positive_valence"].append(sent_intensity_scores["pos"])
        results_during["Neutral_valence"].append(sent_intensity_scores["neu"])
        results_during["Negative_valence"].append(sent_intensity_scores["neg"])
        results_during["Compound_sentiment_intensity"].append(sent_intensity_scores["compound"])
# Save results_pre and results_during into two separate csv files.
df_results_pre=pd.DataFrame(results_pre)
df_results_during=pd.DataFrame(results_during)
df_results_pre.to_csv("/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/name_calling_sentiment_scores_pre_COVID.csv")
df_results_during.to_csv("/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/name_calling_sentiment_scores_during_COVID.csv")





