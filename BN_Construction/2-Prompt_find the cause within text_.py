# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 11:04:51 2023

@author: marys
"""


import os
import openai
import time
from tokenize_text import tokenizer


openai.api_key = 'your API Key'
event="supplier bankruptcy"

def write_text_to_file(folder_path, file_name, text):
    """
    Writes the given text to a file within the specified folder.
    
    Args:
    folder_path (str): The path to the folder where the file will be created.
    file_name (str): The name of the file to create.
    text (str): The text to write to the file.
    """
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Construct the full path to the file
    file_path = os.path.join(folder_path, file_name).replace('\\', '/')
    
    # Write the text to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)



def list_folders(directory):
    """
    This function lists all the folders in the given directory.

    :param directory: The path to the directory whose folders you want to list.
    :return: A list of folder names inside the given directory.
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return []

    # List all entries in the directory
    entries = os.listdir(directory)

    # Filter out the folders
    folders = [entry for entry in entries if os.path.isdir(os.path.join(directory, entry))]

    return folders


def get_completion(prompt, model="gpt-4-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]



def find_cause_propmt(event):
    """
    This function gets the name of a folder, with all the news in.
    Then it will generate a json after analyzing all the news as cause-effect pairs

    """
    list_json=[]
    j=0
   
    directory = 'YOUR PATH' + event
    for filename in os.listdir(directory):
      if j<=15:  
        if filename.endswith('.txt'):
            j+=1
            with open(os.path.join(directory, filename), encoding='utf-8') as f:
                print(filename)
                text = f.read()
                chunks = tokenizer(text,12000).tokenize_text()
                for i, chunk in enumerate(chunks):
                    if i==0:
                        prompt = f"""
                        does  this text, 
                        which is delimited with triple backticks, provide any causes for {event}?
                        answer with yes or no.
                        if yes, 
                        1- can you extract the causal pairs? 
                        2- The cause and effect need  to be an event in two or three words. 
                        3- Put the event information in structured format.
                        For example: Consider the following sentence:
                        
                        "Apple Inc. announced the release of the iPhone 13 in California on September 14, 2021."
                        
                        An event extraction system would identify and extract the following information from this sentence:
                        
                        Event Type: Product Launch
                        Event Trigger: "announced the release"
                        Participants (Arguments):
                        Organizer: Apple Inc.
                        Product: iPhone 13
                        Location: California
                        Date: September 14, 2021
                        4- Also, can you put them in the order of causal hierarchy in a list in  json format? for example:\
                         
                           "cause": "heavy rain",
                            "effect":"flood"
                            
                            "cause": "flood",
                            "effect":"road closure"
                            so we can put them together to find the causal chain of {event} and the final cause effect pair, shows the {event} as the effect.
                         in this example heavy rain causes flood, and flood causes road closure, and road closure cases {event} which is our event,\
             
                        
                          ```{chunk}```
                        """
                try:
                    response = get_completion(prompt)
                    # print(response) 
                    time.sleep(20)
                    prompt = f"""
                    from this response which is in triple backticks, seperate only the causal hierarchy of the json section and return that in json format mentioning cause and effect:
                      
                        ```{response}```
                        
                        
                    """
                    response = get_completion(prompt)
                    list_json.append(response)
                    # print(list_json)
                    
                    time.sleep(20)
                except Exception as e:
                    print("exception: {e}" + str(e))
                
    prompt = f"""
    I give you a list of json items, every single json item  shows the causal relationship of 
    events that end to {event}.
    1- Can you integrate all of them  that end to {event}?
    the list is in triple backticks:
    2- return the final output, as a json of cause and effect pairs   
       ```{list_json}``` 
    3- don't write anythng else in the response just the cause-effect pairs

    """          
    try:
        response = get_completion(prompt) 
    except Exception as e:
        print("again exception: {e}")
    return response

                     # while(answer!=""):
directory = 'YOUR PATH/'+event+'/'+event
list_folders= list_folders(directory)

if len(list_folders)>0:
    for folder in list_folders:
        folder.replace("_", " ")
        cause_effects= find_cause_propmt(folder)
        write_text_to_file(directory+"/" + folder.replace(" ", "_"), "cause_effect_json.txt", cause_effects)
else:
    folder= event
    cause_effects= find_cause_propmt(folder)
    write_text_to_file(directory+"/" + folder, "cause_effect_json.txt", cause_effects)
    
    