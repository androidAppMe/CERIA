# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:53:34 2023

@author: marys
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 09:52:12 2022

@author: marys
"""
from nltk.corpus import wordnet
import numpy as np
import itertools
import pandas as pd
import csv
from NewsCrawler_summary import NewsCrawler_summary
from sentence_transformers import SentenceTransformer, util
model_symmetric = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1', use_auth_token='YOUR TOKEN')


# List_events=['Strike','low wage offer','staff shortage','AFL matches', 'pay cut','COVID','stop in trains','Traffic in roads or highways', 'stop in flights']
List_events=[ 'THE EVENTS FROM THE BN']
dict_seedphrase={}


def split(e):
        list_split=[]
        for i in e.split():
            list_split.append(i)      
        # print(e)
        # print(list_split)
        return list_split



def list_events_synonyms(list_splitted_words, main_event_word):
        # main_event_word=main_event_word
        list_final=[]
        list_event_words=[]
        list_seedphrase=[]
        # list_seedphrase.append(main_event_word)
        for j in list_splitted_words:
            list_synonyms_one_word=synonym_extractor(j)
            if list_synonyms_one_word:
              list_event_words.append(list_synonyms_one_word)
            else:
                list_synonyms_one_word.append(j)
                list_event_words.append(list_synonyms_one_word)
        
        # list_final.append(list_event_words)  
        # print(list_event_words)
        list_final.append(list_event_words)  
        for i in list_final:
           list_combianation_words = list_combination(i)  
           # print(list_combianation_words)
       
        list_new_keywords=[]
        for i in list_combianation_words:
            if len(list_combianation_words)>1:
                if type(i) is tuple:
                    synonym_event=' '.join(i)
                else:
                    synonym_event=i
            else:
                synonym_event=i[0]
            print('synonyms extracted.')
            similarity= findsimilarity(main_event_word, synonym_event)
            mytuple=(synonym_event, similarity)
            list_new_keywords.append(mytuple)
   # dar excel save mishavad:
        write_wordnetResult_in_excel(list_new_keywords, main_event_word)
        for synonym in list_new_keywords:
            if synonym[1]==1:
                list_seedphrase.append(synonym[0])
        
        dict_seedphrase[main_event_word]=list_seedphrase
        
        return dict_seedphrase
 
    
def findNews_addToDict(dict_seedphrase,main_event_word):
     news=NewsCrawler_summary(dict_seedphrase,main_event_word) 
     updated_dict=news.update_dict()
     write_seedphrases_in_excel(updated_dict,main_event_word)
     
     return updated_dict
     
     
     
 
def synonym_extractor(word): 
     synonyms = [] 

     for syn in wordnet.synsets(word):
          for l in syn.lemmas():
              if l.name() not in synonyms:
                  synonyms.append(l.name())
               
     return(synonyms)
        # print(set(synonyms))

def list_combination(List_words):
    if len(List_words)>1:
       list_combination=list(itertools.product(*List_words))
    else:
        if len(List_words[0])==1:   #covid=yes
            list_combination=List_words
        else:
            list_combination=List_words[0]
        
    # print(list_combination)
    return list_combination


def write_wordnetResult_in_excel(list_synonyms, main_event_word):
    filename= main_event_word.replace(" ", "_")
    # print(main_event_word)
    # print(list_synonyms)
    with open('PATH'+ filename + '.csv', 'w', encoding="utf-8") as csvfile:
        csv_out=csv.writer(csvfile)
        csv_out.writerow(['synonym','similarity with main event'])  
        for row in list_synonyms:
            csv_out.writerow(row)
    print("synonyms printed in excel")
    
def write_seedphrases_in_excel(updated_dict,main_event_word):
     filename= main_event_word.replace(" ", "_")
     # print(main_event_word)
     df = pd.DataFrame(updated_dict[main_event_word], columns=["seed_phrases"])
     df.to_csv('PATH'+ filename + '.csv', index=False)
     print("seedphrases printed in excel")
     # with open('C:/Users/marys/OneDrive - UNSW/My PC/python projects/seed_phrases/'+ filename + '.csv', 'w', encoding="utf-8", newline ='') as csvfile:
     #     csv_out=csv.writer(csvfile)
     #     csv_out.writerow(['seed_phrases'])         
     #     for row in updated_dict[main_event_word]:
     #       csv_out.writerows(updated_dict[main_event_word])
     # print("done!")   
    
    
    
def findsimilarity(event, synonym_event):
      query_embedding = model_symmetric.encode(event)
      passage_embedding = model_symmetric.encode(synonym_event)
      similarity=round(util.cos_sim(query_embedding, passage_embedding).item(),2)
      # print("Similarity:", util.cos_sim(query_embedding, passage_embedding)) 
      return similarity
   
list_splitted_words=[]
for i in List_events:
     print(i + " started")
     list_splitted_words=split(i)
     # print(list_splitted_words)
     dict_seedphrase=list_events_synonyms(list_splitted_words, i)     
     findNews_addToDict(dict_seedphrase,i)
# list_events_synonyms(list_total)
# syn=synonym_extractor("road_closure")
# print(syn)