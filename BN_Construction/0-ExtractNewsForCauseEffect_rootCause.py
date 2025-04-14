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

# read the news with a specific keyword by using the synonyms
# extract the keywords of news 
# compare the keywords with seedphrases and score them


# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:57:38 2023

@author: marys
"""
# from keybert import KeyBERT
from pygooglenews import GoogleNews
from newspaper import Article
from newspaper import Config
import nltk
import csv
import re
import os
import sys
sys.setrecursionlimit(1500)  # Increase the recursion limit if needed

import time
import requests
import pandas as pd
from datetime import datetime
from memory_profiler import profile
from symmetric_similarity_score import semantic_similarity


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
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

# kw_model = KeyBERT(model='msmarco-distilbert-base-v4')





USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10 

gn = GoogleNews(lang = 'en')




# df = pd.ExcelFile('C:/Users/marys/OneDrive - UNSW/My PC/python projects/seed_phrases/'+ filename + '.csv').parse(filename) #you could add index_col=0 if there's an index
# seedPhrases.append(df['seed_phrases'])
event='supplier bankruptcy'
event_question='the reasons for '+ event
root= 'YOUR PATH'
list_events=[event_question] 







class FindNewsDaily:
    def __init__(self, list_events):
        
        self.list_events=list_events
       
        # self.list_initial_seedphrases=self.dict_seedphrase[self.main_event]
        
   
    @profile
    def crawl_news(self):
       
       for risk in list_events:
           main_event=risk
           filename= main_event.replace(" ", "_")
           # seedPhrases=[]
           # with open('C:/Users/marys/OneDrive - UNSW/My PC/python projects/seed_phrases/'+ filename + '.csv', 'r') as file:
           #   csvreader = csv.reader(file)
           #   header = next(csvreader)
           #   for line in csvreader:
           #     seedPhrases.append(line[0])
           # stories = []
          
           # # for i in seedPhrases:
           # for j in range(0,2):
           #     i=seedPhrases[j]
             
               # print(intial_seedphrases)
           print("search keyword: " + main_event)
           search_keyword= main_event 
        # search_keyword='"' + i + '"'
           
           # start_date = datetime(2023, 10, 1)
           # end_date = datetime(2023, 10, 1)
            
           # # Format the dates as strings in the format "YYYY-MM-DD"
           # formatted_start_date = start_date.strftime("%Y-%m-%d")
           # formatted_end_date = end_date.strftime("%Y-%m-%d")
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
                       # url = r.url
                       url= get_final_redirect_url(r.url)
                     
                      
                       article = Article(url, config=config)  
                       
                       article.download()
                       
                       
                       article.parse()
                       print(article.authors)
                       body = article.text
                       
                       if body is not None:
                            similarity=semantic_similarity(body,event)
                            similarity_score=similarity.score()
                            print(str(similarity_score))
                            if similarity_score>0.4:
                                 # print(body)
                                 unicode_body = body.encode('utf-8').decode('utf-8')
                                 path =root + event
                                 
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
                        # print("keyword= " + search_keyword)
                   #           print("link= " + item.link)
                            # print(e)
           print('extracting news finished!')
              
            
                      
           # write_news_in_excel(main_event,stories)
       pass
       return 1
                         
    



news=FindNewsDaily(list_events) 
news.crawl_news()

