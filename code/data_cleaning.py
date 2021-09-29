#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 11:32:01 2021

@author: nuoyuan
"""
import pandas as pd
import re
import csv
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string



def remove_retweet(input_file_name,output_file_name):
    f=open(output_file_name,"a+",encoding="utf-8",newline="")
    csv_writer=csv.writer(f) # Create a csv writer object.
    with open(input_file_name,"r+") as g:
        csv_reader=csv.reader(g)
        for line in csv_reader:
            tweet_text=line[4]
            match_result=re.match("RT",tweet_text)
            if match_result==None: # Remove all the retweets from the dataset.
                csv_writer.writerow(line)
    f.close()
          
              
def remove_links(document):
    return re.sub(r"(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|\-)*\b","",document,flags=re.MULTILINE)

def remove_non_ascii(document):
    doc_encode=document.encode("ascii","ignore")
    return doc_encode.decode()

def remove_punctuation(document):
    return document.translate(str.maketrans("","",string.punctuation))

def spell_checking_correction(document):
    return

def abbreviation_detection(document):
    #inf=float("inf")
    re_format=re.compile(r'[A-Z][A-Z]+')
    return re_format.findall(document)

def lower_case(document):
    result=list()
    for unigram in word_tokenize(document):
        result.append(unigram.lower())
    return " ".join(result)


def lemmatize(document):
    def get_wordnet_pos(tag):
        if tag.startswith("J"):
            return wordnet.ADJ
        elif tag.startswith("V"):
            return wordnet.VERB
        elif tag.startswith("N"):
            return wordnet.NOUN
        elif tag.startswith("R"):
            return wordnet.ADV
        else:
            return None
    result=list()
    lemmatizer=WordNetLemmatizer()
    unigrams=word_tokenize(document)
    tagged_sent=pos_tag(unigrams)
    for tag in tagged_sent:
        wordnet_pos=get_wordnet_pos(tag[1]) or wordnet.NOUN
        result.append(lemmatizer.lemmatize(tag[0],pos=wordnet_pos))
    return " ".join(result)

def remove_stopword(document):
    result=list()
    stopwords_en=set(stopwords.words("english"))
    for unigram in word_tokenize(document):
        if unigram not in stopwords_en:
            result.append(unigram)
    return " ".join(result)

        

def term_index_bigram(document,term):
    """
    Parameters
    ----------
    document: the input document.
    term : the term to determine the index of each of its constituting word in the document. Note that it should be a size-2 tuple. 

    Returns
    -------
    This function returns the following tuple: (term, (index of the first constitutenting word, index of the second constitutenting word)).
    """
    first_constitutent_indices=list() # the list of all the indices corresponding to the first word contained in the term of interest. 
    second_constitutent_indices=list() # the list of all the indices corresponding to the second word contained in the term of interest.
    document_unigram=nltk.word_tokenize(document)
    for index,unigram in enumerate(document_unigram):
        if unigram==term[0]: # the index of each occurrence of the first word contained in the term.
            first_constitutent_indices.append(index)
        elif unigram==term[1]: # the index of each occurrence of the second word contained in the term.
            second_constitutent_indices.append(index)
    for index_one in first_constitutent_indices:
        for index_two in second_constitutent_indices:
            if index_one==index_two-1:
                return (term,(index_one,index_two))
                break

    
def term_index_trigram(document,term):
    """
    Parameters
    ----------
    document: the input document.
    term : the term to determine the index of each of its constituting word in the document. Note that it should be a size-3 tuple. 

    Returns
    -------
    This function returns the following tuple: (term, (index of the first constitutenting word, index of the second constitutenting word, index of the third constitutenting word)).
    """
    first_constitutent_indices=list() # the list of all the indices corresponding to the first word contained in the term of interest. 
    second_constitutent_indices=list() # the list of all the indices corresponding to the second word contained in the term of interest.
    third_constitutent_indices=list()  # the list of all the indices corresponding to the third word contained in the term of interest.
    document_unigram=nltk.word_tokenize(document)
    for index,unigram in enumerate(document_unigram):
        if unigram==term[0]: # the index of each occurrence of the first word contained in the term.
            first_constitutent_indices.append(index)
        elif unigram==term[1]: # the index of each occurrence of the second word contained in the term.
            second_constitutent_indices.append(index)
        elif unigram==term[2]: # the index of each occurrence of the third word contained in the term.
            third_constitutent_indices.append(index)
    for index_one in first_constitutent_indices:
        for index_two in second_constitutent_indices:
            for index_three in third_constitutent_indices:
                if (index_one==index_two-1) and (index_two==index_three-1):
                    return (term,(index_one,index_two,index_three))
                    break
            
def term_detection_bigram(document,bigram_terms_bank):
    """
    Parameters
    ---------- 
    document_ungiram: the input document. 
    bigram_terms_bank: the set of bigram terms s.t. each term is stored as a tuple (e.g., the term "united nation" would be stored as ("united","nation")).

    Returns
    -------
    bigram_terms: the list of bigram term-index tuples contained in the input document.
    """
    bigram_terms=list()
    document_unigram=nltk.word_tokenize(document)
    iterator=nltk.bigrams(document_unigram)
    for candidate in iterator:
        if candidate in bigram_terms_bank:
            bigram_terms.append(term_index_bigram(document,candidate))
    return bigram_terms
    
    
def term_detection_trigram(document,trigram_terms_bank):
    """
    Parameters
    ----------
    document_unigram: the input document as a list of unigrams
    trigram_terms_bank: the set of trigram terms s.t. each term is stored as a tuple(e.g.,the term "world health organization" would be stored as ("world","health","organization")).
    
    Returns
    -------
    trigram_terms: the list of trigram term-index tuples contained in the input document.
    """
    trigram_terms=list()
    document_unigram=nltk.word_tokenize(document)
    iterator=nltk.trigrams(document_unigram)
    for candidate in iterator:
        if candidate in trigram_terms_bank:
            trigram_terms.append(term_index_trigram(document,candidate))
    return trigram_terms

def term_concatenation(document,bigram_terms_bank,trigram_terms_bank):
    """
    Parameters
    ----------
    document: the input document. 
    bigram_terms_bank: the set of bigram terms s.t. each term is stored as a tuple (e.g., the term "united nation" would be stored as ("united","nation")). 
    trigram_terms_bank: the set of trigram terms s.t. each term is stored as a tuple(e.g.,the term "world health organization" would be stored as ("world","health","organization")).

    Returns
    -------
    document_tokenized: the tokenized representation of a document with common bi/trigram terms concatenated into single tokens (e.g., given document="world health organization international organization deovting itself to public health crisis monitoring and management",
                        document_tokenized=["world health organization","international organization","devoting","itself","public health crisis","monitoring","management"]. 

    """
    document_tokenized=list()
    document_unigram=nltk.word_tokenize(document)
    terms_list=term_detection_bigram(document,bigram_terms_bank)+term_detection_trigram(document,trigram_terms_bank)
    terms_list_sorted=sorted(terms_list,key=lambda x:x[1][0],reverse=False)
    if len(terms_list_sorted)==0:
        return document_unigram
    else:
        left_index=0
        for term in terms_list_sorted:
            right_index=term[1][0]
            term_str=""
            for idx, word in enumerate(term[0]):
                if idx==len(term[0])-1:
                    term_str+=word
                else:
                    term_str+=word+" "
            for unigram in document_unigram[left_index:right_index]:
                document_tokenized.append(unigram)
            document_tokenized.append(term_str)
            left_index=term[1][-1]+1
        if terms_list_sorted[-1][1][-1]<len(document_unigram)-1:
            for unigram in document_unigram[terms_list_sorted[-1][1][-1]+1:]:
                document_tokenized.append(unigram)
        return document_tokenized


def tokenization(document_tokenized):
    """

    Parameters
    ----------
    document_tokenized: the tokenized representation of a document with common bi/trigram terms concatenated into single tokens (e.g., given document="world health organization international organization deovting itself to public health crisis monitoring and management",
                        document_tokenized=["world health organization","international organization","devoting","itself","public health crisis","monitoring","management"].
    Returns
    -------
    document_uni_bi_tri: the tokenized representation of a document as a list of unigrams, bigrams, and trigrams.
    """
    document_uni=document_tokenized
    document_bi=list()
    document_tri=list()
    for bigram in nltk.bigrams(document_tokenized):
        document_bi.append(bigram[0]+" "+bigram[1])
    for trigram in nltk.trigrams(document_tokenized):
        document_tri.append(trigram[0]+" "+trigram[1]+" "+trigram[2])
    return document_uni+document_bi+document_tri
    
def preprocessing_classification(document):
    bigram_terms_bank={("white","house"),("united","states"),
                  ("united nations"),("social","media"),
                  ("climate","change"),("right","wing"),
                  ("nuclear","power"),("clean","coal"),
                  ("gun violence"),("national","security"),
                  ("tax","cut"),("cut","taxes"),
                  ("president","trump"),("american","people"),
                  ("trump","administration"),("health","care"),
                  ("health","insurance"),("single","payer"),
                  ("assault","weapon"),("assualt","weapons"),
                  ("semi","automatic"),("second","amendment"),
                  ("brady","bill"),("bump","stock"),
                  ("bump","stocks"),("background","check"),
                  ("background","checks"),("wall","funding"),
                  ("birthright citizenship"),("nuclear","deal"),
                  ("pro","life"),("pro","choice"),
                  ("anti","choice"),("born","alive"),
                  ("partial","birth"),("late","term"),
                  ("house","democrats"),("house","republicans"),
                  ("senate","democrats"),("senate republicans"),
                  ("majority","leader"),("minority","leader"),
                  ("town","hall"),("donald","trump"),
                  ("social","security"),("law","enforcement"),
                  ("preexisting","conditions"),("supply","chain"),
                  ("shelter","place"),("laid","off"),
                  ("wish","list"),("op","ed")}
    trigram_terms_bank={("green","new","deal"),("cap","and","trade"),
                   ("medicare","for","all"),("high","capacity","magazine"),
                   ("high","capacity","magazines"),("build","the","wall"),
                   ("world","health","organization"),("center","disease","control"),
                   ("defense","production","act"),("personal","protective","equipment"),
                   ("wash","your","hands")}
    document=remove_links(document)
    document=remove_non_ascii(document)
    document=remove_punctuation(document)
    document=lower_case(document)
    document=lemmatize(document)
    document=remove_stopword(document)
    document_tokenized=term_concatenation(document,bigram_terms_bank,trigram_terms_bank)
    document_uni_bi_tri=tokenization(document_tokenized)
    return document_uni_bi_tri
    
    
def preprocessing_topic_modeling(document):
    bigram_terms_bank={("white","house"),("united","states"),
                  ("united nations"),("social","media"),
                  ("climate","change"),("right","wing"),
                  ("nuclear","power"),("clean","coal"),
                  ("gun violence"),("national","security"),
                  ("tax","cut"),("cut","taxes"),
                  ("president","trump"),("american","people"),
                  ("trump","administration"),("health","care"),
                  ("health","insurance"),("single","payer"),
                  ("assault","weapon"),("assualt","weapons"),
                  ("semi","automatic"),("second","amendment"),
                  ("brady","bill"),("bump","stock"),
                  ("bump","stocks"),("background","check"),
                  ("background","checks"),("wall","funding"),
                  ("birthright citizenship"),("nuclear","deal"),
                  ("pro","life"),("pro","choice"),
                  ("anti","choice"),("born","alive"),
                  ("partial","birth"),("late","term"),
                  ("house","democrats"),("house","republicans"),
                  ("senate","democrats"),("senate republicans"),
                  ("majority","leader"),("minority","leader"),
                  ("town","hall"),("donald","trump"),
                  ("social","security"),("law","enforcement"),
                  ("preexisting","conditions"),("supply","chain"),
                  ("shelter","place"),("laid","off"),
                  ("wish","list"),("op","ed")}
    trigram_terms_bank={("green","new","deal"),("cap","and","trade"),
                   ("medicare","for","all"),("high","capacity","magazine"),
                   ("high","capacity","magazines"),("build","the","wall"),
                   ("world","health","organization"),("centers","disease","control"),
                   ("defense","production","act"),("personal","protective","equipment"),
                   ("wash","your","hands")}
    document=remove_links(document)
    document=remove_non_ascii(document)
    document=remove_punctuation(document)
    document=lower_case(document)
    document=lemmatize(document)
    document=remove_stopword(document)
    document_tokenized=term_concatenation(document,bigram_terms_bank,trigram_terms_bank)
    return document_tokenized

                    


