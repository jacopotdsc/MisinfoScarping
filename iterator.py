import json
from msilib.schema import Directory
import os
from pickle import GLOBAL
from tkinter.tix import DirList
from tracemalloc import start
from unittest import result
import html_check as hc
from time import sleep
import pandas as pd
import time


#### GLOBAL VARIABLE
GLOBAL_DIRECTORY1 = "C:\\Users\\pc\\Desktop\\dataset thesys project\\try_folder_scan" 
GLOBAL_DIRECTORY2 = "C:\\My Web Sites\\factanews\\facta.news" 
GLOBAL_DIRECTORY3 = "C:\\My Web Sites\\factanews"
GLOBAL_DIRECTORY4 = "C:\\My Web Sites"  # bigger one
GLOBAL_DIRECTORY5 = "C:\\misinfo"   

# set this variabile to choose to path to analize
USE_DIRECTORY = GLOBAL_DIRECTORY4

#### VARIABLE STATUS SCANN ####
PRINT_SCAN_STATUS = True   # to print status of iteration
VAR_SLEEP = 0.0            # variabile to read print of scan
AUXLIARY_FOR_FORMAT = 0     # variable for print
FREQ = 500                  # every how much print status
HTML_EXAMINATED = 0         # counter for html examinated
FOLDER_SCANNED = 0          # counter for folder scanned
TOTAL_FILE_SCANNED = 0      # counter for total scan / iteration
TOTAL_CLAIM_REVIEW_FILE = 0 # number of claim reviewed file

def increment_claim_reviewed_json():
    global TOTAL_CLAIM_REVIEW_FILE

    TOTAL_CLAIM_REVIEW_FILE = TOTAL_CLAIM_REVIEW_FILE + 1

def increment_total_file_scanned():
    global TOTAL_FILE_SCANNED
    
    TOTAL_FILE_SCANNED = TOTAL_FILE_SCANNED + 1

    if AUXLIARY_FOR_FORMAT % FREQ == 0 and AUXLIARY_FOR_FORMAT > 500:
        if PRINT_SCAN_STATUS == True:
            print("-- total file scanned until now: " + str(TOTAL_FILE_SCANNED))
            sleep(VAR_SLEEP)

def increment_html_examinated():
    global HTML_EXAMINATED
    global AUXLIARY_FOR_FORMAT

    HTML_EXAMINATED = HTML_EXAMINATED + 1
    AUXLIARY_FOR_FORMAT = AUXLIARY_FOR_FORMAT + 1

    if AUXLIARY_FOR_FORMAT % FREQ == 0:
        if PRINT_SCAN_STATUS == True:
            print("-- html file examinated until now: " + str(HTML_EXAMINATED)) 
            sleep(VAR_SLEEP)

def increment_folder_scannned():
    global FOLDER_SCANNED

    FOLDER_SCANNED = FOLDER_SCANNED + 1

    if AUXLIARY_FOR_FORMAT % FREQ == 0 and AUXLIARY_FOR_FORMAT > 500:
        if PRINT_SCAN_STATUS == True:
            print("-- total folder scanned until now: " + str(FOLDER_SCANNED))
            sleep(VAR_SLEEP)

html_array = []

def make_flat_dict(json_file, new_dict, depth=0):

    #print(type(json_file))
    #print(json_file)

    #print()
    #print("key_list: " + str(json_file.keys()) )
    for key in json_file.keys():        # scan every key
        
        value = json_file[key]
        #print("key: " + str(key) + " -> " + str(value))
        

        if str(  type(value)  ) == "<class 'dict'>":
            #print("-- dict:  recursion on dict, " + str(type(value)))
            make_flat_dict(value, new_dict,depth+1)

        elif str(  type(value)  ) == "<class 'list'>":    # if it's a list, # check if list of dict

            #print("--- list: recursion on list, " + str(type(value)))
            for elem in value:
                if str(type(elem)) == "<class 'str'>":
                    new_key = key + "." + str(depth)
                    new_dict[new_key] = []
                    new_dict[new_key].append(elem)
                else:
                    make_flat_dict(elem,new_dict, depth + 1)
        else:
            #print("--- str: append,  " + str(type(value)))
            new_key = str(key) + "." + str(depth)

            if new_key in new_dict.keys():
                new_dict[new_key].append(value)
            else:
                new_dict[new_key] = []
                new_dict[new_key].append(value)

    return new_dict



def iterate_on_folders(directory):

    dir_list = os.listdir(directory)
    for filename in dir_list:

        increment_total_file_scanned()

        # analize html
        if filename.endswith(".html"):  
            new_path = directory + "\\" + filename
            result = hc.get_claimReviewed_scheme_in_html_code(new_path)
            
            # result is an array of < [ json_file, ... ], lang >     
            for file_json in result[0]:

                if file_json == []:
                    break
                else:
                    increment_claim_reviewed_json()

                new_json = file_json
                new_json['lang'] = result[1]

                new_dict = {} 
                flattend_dict = make_flat_dict(new_json, new_dict)
            
                html_array.append(flattend_dict)

            increment_html_examinated()


        elif os.path.isdir(str(directory) + "\\" + filename) == True:
            new_path = str(directory) + "\\" + filename

            increment_folder_scannned()
            try:
                iterate_on_folders(new_path)
            except:
                continue
    

def create_csv(dataframe):
    if USE_DIRECTORY == GLOBAL_DIRECTORY1:
        dataframe.to_csv("data_prova.csv")
    else:
        dataframe.to_csv("data.csv")
    
def create_dataset(data_array):
    return pd.DataFrame(data_array).sort_index(axis=1)

def main():

    start_time = time.time()
    iterate_on_folders(USE_DIRECTORY)
    end_time = time.time() 
    total_time = end_time - start_time
    #print("total_time: %s" + str(total_time))
    print(total_time)
    
    '''
    result = hc.get_claimReviewed_scheme_in_html_code("try_folder_scan\\mucche_latte.html")

    print(result[0][0])
    print(len(result[0]))
    for file_json in result[0]:
        new_json = file_json
        new_json['lang'] = result[1]

        new_dict = {} 
        flatten_dict = make_flat_dict(new_json, new_dict)

        
        print("flatten dict")


        for k in flatten_dict.keys():
            print("-- " + str(k) +  " -> " + str(flatten_dict[k]) )
        print()
    '''
        

    print("\ntotal html file examinated: " + str(HTML_EXAMINATED))
    print("total folder scanned: " + str(FOLDER_SCANNED))
    print("total file scanned: " + str(TOTAL_FILE_SCANNED))
    print("total json claim reviewed found: " + str(TOTAL_CLAIM_REVIEW_FILE))

    dataset = create_dataset(html_array)
    #print(dataset.head())
    create_csv(dataset)


main()


