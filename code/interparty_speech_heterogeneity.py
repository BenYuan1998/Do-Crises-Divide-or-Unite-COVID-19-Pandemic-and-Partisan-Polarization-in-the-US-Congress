#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:11:07 2021

@author: nuoyuan
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import tqdm


# Write a function that returns a list of all hyperparameter permutations given a hyperparameter grid.
def param_perm(param_grid):
    param_combinations=list()
    import itertools
    keys,values=zip(*param_grid.items())
    for value in itertools.product(*values):
        param_combinations.append(list(value))
    return param_combinations


def hyperparameter_tuning_cv(data_path,corpus_name,param_grid,n_splits=10):
    """
    Parameters
    ----------
    data_path: The path of the corpus on which to fine-tune a random forest classifier.
    corpus_name: The name of the corpus.
    param_grid: The grid of hyperparameters and their respective candidate values. Note that param_grid should be a dictionary.
    n_splits: The number of folds for stratified cross-validation. The default is set to be 10.

    Returns
    -------
    results:
    """
    param_combinations=param_perm(param_grid)
    results={"corpus":[],
             "hyperparameter combination":[],
             "number of folds":[],
             "average cross-validated accuracy score":[]}
    df=pd.read_csv(data_path,header=0)
    # Code the binary party_affiliation target variable by using 0 to denote Democratic-authored tweets and 1 to denote Republican-authored tweets.
    code_dict={"Democratic":0,
               "Republican":1
               }
    df["party_affiliation"]=df["party_affiliation"].map(code_dict)
    # Split df into feature variables and target variable. 
    y=df["party_affiliation"]
    non_feature_columns=["party_affiliation","created_at"]
    X=df.drop(columns=non_feature_columns,inplace=False)
    # Randomly split X and y into as many stratified folds that preserve class percentage as specified by n_splits.
    stratified_cv=StratifiedKFold(n_splits=n_splits,shuffle=True,random_state=42)
    pbar=tqdm.tqdm(total=len(param_combinations))
    for permutation in param_combinations:
        accuracies=list()
        n_estimators=permutation[0]
        hyperparameters={"number of estimators":n_estimators}
        rf=RandomForestClassifier(n_estimators=n_estimators)
        for train_indices,test_indices in stratified_cv.split(X,y):
            X_train,X_test=X.iloc[train_indices],X.iloc[test_indices]
            y_train,y_test=y.iloc[train_indices],y.iloc[test_indices]
            # Train a random forest classifier on X_train and y_train with as many decision-tree base classifiers as specified by n_estimators.
            rf.fit(X_train,y_train)
            y_pred=rf.predict(X_test)
            # Evaluate the performance of the trained random forest classifier via accuracy.
            accuracy=accuracy_score(y_test,y_pred)
            accuracies.append(accuracy)
        avg_accuracy=np.mean(accuracies)
        results["corpus"].append(corpus_name)
        results["hyperparameter combination"].append(hyperparameters)
        results["number of folds"].append(n_splits)
        results["average cross-validated accuracy score"].append(avg_accuracy)
        pbar.update(1)
    pbar.close()
    return results
def experiment(data_path,corpus_name,n_estimators,n_splits=10):
    results={"corpus":[],
             "round of experiment":[],
             "number of base estimators":[],
             "accuracy score":[]
             }
    df=pd.read_csv(data_path,header=0)
    # Code the binary party_affiliation target variable by using 0 to denote Democratic-authored tweets and 1 to denote Republican-authored tweets.
    code_dict={"Democratic":0,
               "Republican":1
               }
    df["party_affiliation"]=df["party_affiliation"].map(code_dict)
    # Split df into feature variables and target variable. 
    y=df["party_affiliation"]
    non_feature_columns=["party_affiliation","created_at"]
    X=df.drop(columns=non_feature_columns,inplace=False)
    # Randomly split X and y into as many stratified folds that preserve class percentage as specified by n_splits.
    stratified_cv=StratifiedKFold(n_splits=n_splits,shuffle=True,random_state=30)
    rf=RandomForestClassifier(n_estimators=n_estimators)
    cur_round=1
    pbar=tqdm.tqdm(total=n_splits)
    for train_indices,test_indices in stratified_cv.split(X,y):
        X_train,X_test=X.iloc[train_indices],X.iloc[test_indices]
        y_train,y_test=y.iloc[train_indices],y.iloc[test_indices]
        # Train a random forest classifier on X_train and y_train with as many decision-tree base classifiers as specified by n_estimators.
        rf.fit(X_train,y_train)
        y_pred=rf.predict(X_test)
        # Evaluate the performance of the trained random forest classifier via accuracy.
        accuracy=accuracy_score(y_test,y_pred)
        results["corpus"].append(corpus_name)
        results["round of experiment"].append(str(cur_round)+"th round")
        results["number of base estimators"].append(n_estimators)
        results["accuracy score"].append(accuracy)
        cur_round+=1
        pbar.update(1)
    pbar.close()
    results=pd.DataFrame(results)
    return results

if __name__=="__main__":
    path_pre="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/document_term_matrix_pre_covid_classification.csv"
    path_during="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/data_crisis_events_removed/document_term_matrix_during_covid_classification.csv"
    name_pre="pre-COVID corpus"
    name_during="during-COVID corpus"
    #param_grid={"n_estimators":[100,200,300,400,500,600,700,800,900,1000]}
    optimal_estimators_pre=500
    optimal_estimators_during=900
    results_pre=experiment(path_pre,name_pre,optimal_estimators_pre)
    results_during=experiment(path_during,name_during,optimal_estimators_during)
    print(results_pre)
    print(results_during)
    #print(hyperparameter_tuning_cv(data_path=path_pre,corpus_name=name_pre,param_grid=param_grid))
    #print(hyperparameter_tuning_cv(data_path=path_during,corpus_name=name_during,param_grid=param_grid))
        

        
    
    
    