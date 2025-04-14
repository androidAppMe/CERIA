# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:17:16 2024

@author: marys
"""

import json
import re
import csv
import os
import pandas as pd
import json

directory = 'YOUR PATH'

output_file_path = 'YOUR PATH2'

def list_folders(directory):
    """
    This function lists all the folders in the given directory.

    :param directory: The path to the directory whose folders you want to list.
    :return: A list of folder names inside the given directory.
    """
    # Check if the directory exists
    folder_list = []

    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(directory):
        for dirname in dirnames:
            folder_list.append(os.path.join(dirpath, dirname))

    return folder_list

def Collect_source_target_from_json(input_folder, all_pairs):
    input_file_path = (input_folder +'/cause_effect_json.txt').replace('\\', '/')
    if os.path.isfile(input_file_path):
   
        with open(input_file_path, 'r') as file:
            content = file.read()
        
        # Regular expression to find cause-effect pairs
        pattern = re.compile(r'\{\s*"cause":\s*"(.*?)",\s*"effect":\s*"(.*?)"\s*\}', re.DOTALL)
        matches = pattern.findall(content)
        all_pairs.extend(matches)
    # Write the cause-effect pairs to a CSV file
 
    
all_pairs = []
list_folders= list_folders(directory)


for folder in list_folders:
       Collect_source_target_from_json(folder,all_pairs)
       
       
       
with open(output_file_path+'/final_cause_effect_json.csv', 'w', newline='') as csvfile:
           fieldnames = ['source', 'target']
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
       
           writer.writeheader()
           for cause, effect in all_pairs:
               writer.writerow({'source': cause, 'target': effect})
unique_values = set()
for cause, effect in all_pairs:
        unique_values.add(cause)
        unique_values.add(effect)
with open(output_file_path+'/next_level_nodes.csv', 'w', newline='') as csvfile:
           
       writer = csv.writer(csvfile)
        # Write header
       for value in sorted(unique_values):
           writer.writerow([value])

df = pd.read_csv(output_file_path+'/final_cause_effect_json.csv')

# Assuming the CSV has columns 'source' and 'target'
data = []

for index, row in df.iterrows():
    data.append({
        "source": row['source'],
        "target": row['target']
    })

# Convert the list to a JSON string with indentation for readability
json_data = json.dumps(data, indent=4)

with open(output_file_path +'/node_list.txt', 'w', newline='') as textfile:
          textfile.write(json_data)     
print(f'Cause-effect pairs have been written to {output_file_path}')