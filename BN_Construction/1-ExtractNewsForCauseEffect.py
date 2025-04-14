# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 16:05:46 2023

@author: marys
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 11:01:11 2023

@author: marys
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:57:38 2023

@author: marys
"""
# from keybert import KeyBERT
from pygooglenews import GoogleNews
from selenium import webdriver
from newspaper import Article
from newspaper import Config
from time import sleep
from newspaper.article import ArticleException, ArticleDownloadState
import nltk
import csv
import re
import os
import time
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from memory_profiler import profile
from symmetric_similarity_score import semantic_similarity
# from symmetric_similarity_score import semantic_similarity
nltk.download('punkt')

# kw_model = KeyBERT(model='msmarco-distilbert-base-v4')





USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

gn = GoogleNews(lang = 'en')

def get_final_redirect_url(url):


    # service = service = Service("/snap/bin/firefox.geckodriver")
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely
        final_url = driver.current_url
    except Exception as e:
        print(f"An error occurred: {e}")
        final_url = None
    finally:
        driver.quit()
    print(final_url)
    return final_url
# from symmetric_similarity_score import semantic_similarity
nltk.download('punkt')

class FindNewsDaily:
    def __init__(self, list_events):
       
        self.list_events=list_events
       
        # self.list_initial_seedphrases=self.dict_seedphrase[self.main_event]
       
   
    @profile
    def crawl_news(self):
       
       for event in list_events:
           
           filename= event.replace(" ", "_")
           
           print("search keyword: " + event)
           search_keyword='the reasons for '+ event
       
           search = gn.search(search_keyword, when ='2y') #from_='2020-07-01', to_='2029-07-02') #when: duration; 2y = 2 years, 6m = 6 months, etc.
           # gn.set_encode('utf-8')
           newsitem = search['entries']
           i=0
           print(len(newsitem))
           for item in newsitem:
                    i+=1
                    print(str(i))
                    try:
                       
                       r = requests.get(item.link, timeout=10)
                       
                       time.sleep(1)
                       
                       # story = item.link
                       url = r.url
                       # # url="https://www.usnews.com/news/national-news/articles/2024-07-19/what-happens-to-bidens-campaign-money-if-he-drops-out"
                       # url = urlparse(url)
                       # url_f=parse_qs(url.query)['url'][0]
                       url= get_final_redirect_url(r.url)
                       article = Article(url, config=config)  
                       
                       article.download()
                       
                     
                       article.parse()
                     
                       body = article.text
                       
                       if body is not None:
                           
                            similarity=semantic_similarity(body,event)
                            similarity_score=similarity.score()
                            if similarity_score>0.4:
                                 # print(body)
                                 unicode_body = body.encode('utf-8').decode('utf-8')
                                 path ='YOUR PATH'+event.replace(' ', "_")+'/'
                                 
                                 # Path
                                 # path = os.path.join(parent_dir, directory)
                                 isExist = os.path.exists(path)
                                 if isExist:
                                     print('folder exists!')
                                 else:
                                     os.mkdir(path)
                                 with open(path+'/'+str(i)+'.txt', 'w', encoding="utf-8") as file:
                                    # Write a string into the file
                                   # print(body)
                                   file.write(unicode_body)
                                 file.close()
                       newsitem.remove(item)
                                 
                    except Exception as error:
   
                            print("An exception occurred:", error)
                       
           print('extracting news finished!')
               
       pass
       return 1
                         
list_events=[]
with open('PATH/next_level_nodes.csv', mode='r') as file:
    # Create a CSV DictReader object
    csv_reader = csv.reader(file)
   
    # Loop through the rows in the CSV reader
    for row in csv_reader:
        list_events.append(row[0])

for event in list_events:
   
   
    news=FindNewsDaily(event)
    news.crawl_news()