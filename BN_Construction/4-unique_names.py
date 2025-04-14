# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:39:15 2024

@author: marys
This file get the names of the nodes  and unifys them if they're similar' 
"""

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from graph_source_target import myGraphPng
from networkX_from_source_target import NetworkXHtml
from NextLevel import NextLevelGraph
import csv
import sys
from symmetric_similarity_score import semantic_similarity
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1', use_auth_token='YOUR TOKEN')
print("1")
# with open("console_output_second_part.txt", "w") as log_file:
#     # Save the current stdout so that we can revert sys.stdout after we're done
#     print("2")
#     original_stdout = sys.stdout
    
#     # Redirect stdout to the file
#     sys.stdout = log_file
#     print("3")
event="delay in delivery"    
with open("YOUR PATH"+event+"/"+event+"/node_list.txt", mode='r') as file:
    data = file.read()
    data=json.loads(data)
    print("2")
# Step 1: Extract Unique Node Names
node_names = set()
unique_json = set(json.dumps(d, sort_keys=True) for d in data)
unique_data = [json.loads(d) for d in unique_json]
for item in unique_data:
    node_names.update([item["source"], item["target"]])
node_names = list(node_names)

threshold=0.737 
similar_groups = {}
for i in range(len(node_names)):
   print("i:" + str(i))
   if node_names[i] not in similar_groups and node_names[i] not in similar_groups.values():
   # if node_names[i] not in  similar_groups.values():
        list_similars_to_i=[]
        list_similars_to_i.append(node_names[i])
        list_j_index=[]
        for j in range(0 , len(node_names)):
            
            # similarity = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
            similarity_object = semantic_similarity(node_names[i], node_names[j])
            similarity = similarity_object.score()
            # print("i: " + str(i))
            # print("j: " + str(j))
            # print("node_names[i]: " + node_names[i])
            # print("node_names[j]: " + node_names[j])
            # print("similarity: " + str(similarity))
            # round(util.cos_sim(query_embedding, passage_embedding).item(),3)
            if similarity >= threshold:
                
                list_similars_to_i.append(node_names[j])
                list_j_index.append(j)
              
                # if len(node_names[i])< len(node_names[j]):
                #     similar_groups[node_names[j]] = node_names[i]
                # else:
                #     similar_groups[node_names[i]] = node_names[j]
        for x in list_similars_to_i:
            if x in similar_groups: 
                shortest_item= similar_groups[x]
                print("yes this happened")
                print("i: " + node_names[i])
                print("j:" + node_names[j])
        else:
            shortest_item = min(list_similars_to_i, key=len)
        for k in list_similars_to_i:
            # print("for " + k + ": " + shortest_item)
            similar_groups[k] = shortest_item
        
       # # for all thenodes, change their name.  
       #  for x in list_j_index:
       #     node_names[x]=shortest_item
with open('my_dict'+ datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+str(threshold)+'.txt', 'w') as file:
    json.dump(similar_groups, file)

j=0
new_nodes=[]
with open("YOUR PATH2" + event + "/" + event +  "/equivalents_" + event + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+".csv", 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['name', 'equivalent'])
    for item in unique_data:
        
        source = similar_groups[ item["source"] ]
        target = similar_groups[ item["target"] ]
        # print("item(source): "+ item["source"] )
        # print("dic(source): "+ similar_groups[ item["source"] ])
        # print("item(target): " + item["target"] )
        # print("dic(target): " + similar_groups[ item["target"] ])
        new_tuple = (source, target)
        new_nodes.append(new_tuple)
        
        csvwriter.writerow([item["source"], similar_groups[ item["source"] ]])
        csvwriter.writerow([item["target"] , similar_groups[ item["target"] ]])
        
        
with open("YOUR PATH2"+event + "/"+ event + "/graph-"+ event +datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+".csv", mode='w', newline='') as file:

    writer = csv.writer(file)
    # writer.writerow(["source", "target"])
    # Writing the header with fieldnames
    for item in new_nodes:
        writer.writerow(item)    
    
 
# sys.stdout = original_stdout    



  
# fieldnames = data[0].keys()
# with open("C:/Users/marys/OneDrive - UNSW/My PC/python projects/get news for different events_test version with Omar/cause-effect/delay in delivery/graph-delivery-delays"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+".csv", mode='w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()  # Writing the header with fieldnames
#     for item in unique_data:
#         writer.writerow(item)
# NextLevelGraph(data, "delivery delays").buildNextLevel()


