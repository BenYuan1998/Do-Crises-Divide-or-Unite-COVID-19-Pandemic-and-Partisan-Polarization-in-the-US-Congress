#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 11:00:43 2021

@author: nuoyuan
"""
import re
import csv
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import pandas as pd
from data_cleaning import preprocessing_classification
from sklearn.feature_extraction.text import CountVectorizer


# Load and store the the pre-COVID and during-COVID corpora into two separate pandas dataframe objects.
path_pre="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_pre_covid_retweets_removed.csv"
path_during="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/tweets_during_covid_retweets_removed.csv"
df_pre=pd.read_csv(path_pre,header=0)
df_during=pd.read_csv(path_during,header=0)
tweets_pre=df_pre["tweet_text"].values
party_pre=df_pre["party_affiliation"]
created_at_pre=df_pre["created_at"]
tweets_during=df_during["tweet_text"].values
party_during=df_during["party_affiliation"]
created_at_during=df_during["created_at"]

# Use the CountVectorizer from sklearn with analyzer set to be preprocessing_classification from data_cleaning.py.
# to construct a document-term matrix (each row in the matrix represents a document/tweet. 
# Each column of the matrix represents a token that appears at least once in the corpus. Lastly,
# each entry (i,j) represents the num of times token j appears in document i) out of each corpus. 
vectorizer_pre=CountVectorizer(analyzer=preprocessing_classification,max_df=0.5,min_df=100)
document_term_matrix_pre=vectorizer_pre.fit_transform(tweets_pre).toarray()
columns_pre=vectorizer_pre.get_feature_names()
document_term_matrix_pre=pd.DataFrame(document_term_matrix_pre,columns=columns_pre)
document_term_matrix_pre["party_affiliation"]=party_pre
document_term_matrix_pre["created_at"]=created_at_pre

vectorizer_during=CountVectorizer(analyzer=preprocessing_classification,max_df=0.5,min_df=100)
document_term_matrix_during=vectorizer_during.fit_transform(tweets_during).toarray()
columns_during=vectorizer_during.get_feature_names()
document_term_matrix_during=pd.DataFrame(document_term_matrix_during,columns=columns_during)
document_term_matrix_during["party_affiliation"]=party_during
document_term_matrix_during["created_at"]=created_at_during

# Store the resulting two document-term matrices into two separate csv files. 
document_term_matrix_pre.to_csv("/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/document_term_matrix_pre_covid_classification.csv",header=True)
document_term_matrix_during.to_csv("/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/document_term_matrix_during_covid_classification.csv",header=True)







