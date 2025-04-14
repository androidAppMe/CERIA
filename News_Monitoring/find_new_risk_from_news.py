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
from keybert import KeyBERT
from pygooglenews import GoogleNews
from newspaper import Article
from newspaper import Config
import nltk
import csv
import re
import os
import time
import requests
import pandas as pd
from symmetric_similarity_score import semantic_similarity
nltk.download('punkt')


kw_model = KeyBERT(model='msmarco-distilbert-base-v4')





USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Geck/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10 

gn = GoogleNews(lang = 'en')




# df = pd.ExcelFile('C:/Users/marys/OneDrive - UNSW/My PC/python projects/seed_phrases/'+ filename + '.csv').parse(filename) #you could add index_col=0 if there's an index
# seedPhrases.append(df['seed_phrases'])

list_events=['LIST OF THE EVENTS'] 

# "airport staff shortage"
# "construction workers strike"





class FindNewsDaily:
    def __init__(self, list_events):
        
        self.list_events=list_events
       
        # self.list_initial_seedphrases=self.dict_seedphrase[self.main_event]
        
   
    
    def crawl_news(self):
       
       for risk in list_events:
           main_event=risk
           filename= main_event.replace(" ", "_")
           seedPhrases=[]
           with open('PATH TO SEED PHRASES'+ filename + '.csv', 'r') as file:
             csvreader = csv.reader(file)
             header = next(csvreader)
             for line in csvreader:
               seedPhrases.append(line[0])
           stories = []
          
           # for i in seedPhrases:
           for j in range(0,2):
               i=seedPhrases[j]
             
               # print(intial_seedphrases)
               print("seedphrase: " + i)
               search_keyword= i 
               # search_keyword='"' + i + '"'
               
              
               search = gn.search(search_keyword, from_ = "2021-10-01", to_ = "2023-10-03") #when: duration; 2y = 2 years, 6m = 6 months, etc. 
               newsitem = search['entries']
               for item in newsitem:
          
                     try: 
                      
                       r = requests.get(item.link)
                       time.sleep(1)
                       # story = item.link
                       url = r.url
                       print("url: " + url)
                       article = Article(url, config=config)       
                       article.download()
                       article.parse()
                       body = article.text
                       if body is not None:
                         
                            
                             title = item.title
                            
                             summary=article.summary
                            
                             keywords = kw_model.extract_keywords(body, 
           
                                                keyphrase_ngram_range=(1, 3), 
           
                                                stop_words='english', 
           
                                                highlight=False,
           
                                                top_n=10)
           
                             keywords_list= list(dict(keywords).keys())
                             # ----------------------summery by sbert
                            
                             
                             
                             # -------------------------
                             listToStr_keywords = ','.join([str(elem) for i,elem in enumerate(keywords_list)])
                             
                             
                             
                             
                             avg_score_news = 0
                             sum_score_news=0
                             for j in keywords_list:
                                 
                                 sum_score_one_keyword=0
                                 avg_score_one_keyword=0
                                 for n in seedPhrases:
                                   similarity=semantic_similarity(j,n)
                                   similarity_score=similarity.score()
                                   # if max_sim<similarity_score:
                                   #     max_sim=similarity_score
                                   sum_score_one_keyword+=similarity_score
                                 avg_score_one_keyword=sum_score_one_keyword/len(seedPhrases)
                                 sum_score_news+=avg_score_one_keyword
                             avg_score_news=round(sum_score_news/len(keywords_list),2)
                             
                             
                             similarity_news_searchKeyword =semantic_similarity(body,main_event).score()
                             
                             
                             news=News(search_keyword, main_event, listToStr_keywords,url,title,avg_score_news, similarity_news_searchKeyword)          
                             # if similarity_news_searchKeyword>0.3:
                             stories.append(news)    
                             print(str(similarity_news_searchKeyword)    )
                             print("one news was analyzed")
                                  
                     except Exception as e:                   
                        print(":(")
                        # print("keyword= " + search_keyword)
                   #           print("link= " + item.link)
                            # print(e)
               print('extractinge news finished!')
              
            
                      
           write_news_in_excel(main_event,stories)
       
       return 1
                         
    
    
def write_news_in_excel(main_event_word, list_news):
          filename= main_event_word.replace(" ", "_")
          # filename=search_keyword.replace(" ", "_")
          
          # Parent Directory path
          path = "YOUR PATH FOR NEWS"
          
          # Path
          # path = os.path.join(parent_dir, directory)
          isExist = os.path.exists(path)
          if isExist:
              print('folder exists!')
          else:
              os.mkdir(path)
          
          # with open('C:/Users/marys/OneDrive - UNSW/My PC/python projects/news_archive/'+ foldername +'/'+ filename + '.csv', 'w') as csvfile:
          with open(path +'/'+ filename + '.csv', 'w', encoding="utf-8") as csvfile:
              csv_out=csv.writer(csvfile)
              csv_out.writerow(['search_keyword','main_event','keywords_list','link','title','avg_score_one_news', 'similarity_news_searchKeyword'])  
              for item in list_news:
                  # csv_out.writerow(row)
                  csv_out.writerow( [item.search_keyword, item.main_event, item.keywords_list, item.link,item.title, item.avg_score_one_news, item.similarity_news_searchKeyword])
          print(" writing news in excel done!")          
          
      
class News:
          
          def __init__(self,search_keyword, main_event, keywords_list,link,title,avg_score_one_news, similarity_news_searchKeyword):
           self.keywords_list= keywords_list 
           self.search_keyword = search_keyword
           self.main_event=main_event
           self.link=link
           self.title=title
           self.avg_score_one_news=avg_score_one_news
           self.similarity_news_searchKeyword=similarity_news_searchKeyword
           
class Seedphrase:
    
        def __init__(self, event, search_keyword, seedphrase, news_link, news_title, similarity_score):
            self.event= event
            self.search_keyword = search_keyword
            self.seedphrase=seedphrase
            self.news_link=news_link
            self.news_title=news_title
            self.similarity_score=similarity_score


news=FindNewsDaily(list_events) 
news.crawl_news()

