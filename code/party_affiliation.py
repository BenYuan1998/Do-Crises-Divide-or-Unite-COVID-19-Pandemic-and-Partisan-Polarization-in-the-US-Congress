#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:27:35 2021

@author: nuoyuan
"""

import wptools


handles_path="/Users/nuoyuan/Desktop/Research_Projects/AI_and_Global_Governance_A_Merit_Stemming_from_a_Crisis_Did_the_COVID_19_Pandemic_Lessen_Partisan_Polarization_in_the_US_Congress/Data/116th_Congress_twitter_handles.txt"

f1=open("116th_Congress_twitter_handles_party_determined.txt","a+")
f2=open("116th_Congress_twitter_handles_party_undetermined.txt","a+")

with open(handles_path,"r") as g:
    for line in g.readlines():
        data=line.split("|")
        name=data[-1]
        name=name.strip().replace("\n","")
        if ("Angus King" in name) or ("Bernie Sanders" in name):
            f1.write("Democratic"+"|"+line)
        elif "Justin Amash" in name:
            f1.write("Republican"+"|"+line)
        else:
            try: # Use a try-except statement to determine whether a Wikpedia page with the given "name" exists.  
                page=wptools.page(name).get_parse()
                data=page.data["infobox"]
                try: # Use a try-except statement to determine whether information indicating the party affiliation of a Wikipedia page associated with some Twitter handle is available in the infobox section.# Use a try-except statement to determine whether information indicating the party affiliation of a Wikipedia page associated with some Twitter handle is available in the infobox section.
                    party=data["party"]
                    if "Democratic" in party:
                        f1.write("Democratic"+"|"+line)
                    elif "Republican" in party:
                        f1.write("Republican"+"|"+line)
                    else:
                        f2.write(line)
                except:
                    f2.write(line)
            except:
                f2.write(line)
f1.close()
f2.close()
            
    