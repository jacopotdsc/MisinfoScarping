from cProfile import label
import chunk
import json
from msilib.schema import Directory
import os
from pickle import GLOBAL
from tkinter.tix import DirList
from tracemalloc import start
from unittest import result
from xml.dom.expatbuilder import DOCUMENT_NODE
from langdetect import detect, DetectorFactory
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rcParams
from sklearn.cluster import KMeans

from time import sleep
import pandas as pd
import time
from nltk.corpus import stopwords
from googletrans import Translator
import math 

import html_check as hc
import nlp_module as nlpm
import lda


#### GLOBAL VARIABLE
GLOBAL_DIRECTORY0 = "try_folder_scan"
GLOBAL_DIRECTORY1 = "C:\\Users\\pc\\Desktop\\dataset thesys project\\try_folder_scan" 
GLOBAL_DIRECTORY2 = "C:\\My Web Sites\\factanews\\facta.news" 
GLOBAL_DIRECTORY3 = "C:\\My Web Sites\\factanews"
GLOBAL_DIRECTORY4 = "C:\\My Web Sites"  # bigger one
GLOBAL_DIRECTORY5 = "C:\\misinfo"   

# set this variabile to choose to path to analize
USE_DIRECTORY = GLOBAL_DIRECTORY0

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


##### START OF CODE ####

html_array = [] # array which contain html text
keywords_array = [] # keywords of articles's tile
title_array = []    # array with title of articles

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


def detect_language(text):
    DetectorFactory.seed = 0
    return detect(text)


# iterator through all folders and call functions for data analisys
def iterate_on_folders(directory):

    dir_list = os.listdir(directory)
    for filename in dir_list:

        increment_total_file_scanned()

        # analize html
        if filename.endswith(".html"):  

            new_path = directory + "\\" + filename  # path of the html_file
            result = hc.get_claimReviewed_scheme_in_html_code(new_path)
            
            # result is an array of < [ json_file, ... ], lang >   
            
            for file_json in result:

                if file_json == []:
                    break
                else:
                    increment_claim_reviewed_json()

                new_dict = {} 

                # taking all keywords from the returned array
                html_keywords, all_url = nlpm.extract_informations(new_path)

                # saving all url interal to the main text
                file_json['internal_url'] = all_url



                # creating my dictionary
                flattend_dict = make_flat_dict(file_json, new_dict)

                string_to_translate = flattend_dict['claimReviewed.0'][0] # article's title

                language = detect_language(string_to_translate)
                flattend_dict['lang'] = language
                

                # append final dictionary
                html_array.append(flattend_dict)

                # append title for word-cloud
                doc_title = flattend_dict['claimReviewed.0'][0]

                
                
                #### word-cloud part , search for keyword

                filtered_words = []
                translator = Translator()
                    
                for word in doc_title.split():
                    #lang = translator.translate(word) 
                    lang = 'italian'
                    my_stopwords = list( stopwords.words(lang ) )
                    if nlpm.check_if_contain_html_words_or_stopwords(word, my_stopwords) == False:
                        filtered_words.append(word)

                #filtered_words = [word for word in doc_title.split() nlpm.check_if_contain_html_words_or_stopwords(word, my_stopwords) == False ]

                #print(type(filtered_words))
                title_array.append(filtered_words)
                keywords_array.append(filtered_words)

                # append keywords for word-cloud
                #new_title = " ".join(chunk for chunk in filtered_words if chunk)
                #print(new_title)
                #keywords_array.append(new_title)
                

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
        dataframe.to_csv("data_prova_2.csv")
    else:
        dataframe.to_csv("data.csv")
    
def create_dataset(data_array):
    return pd.DataFrame(data_array).sort_index(axis=1)

def plot_language_pie_chart(data):

    data_to_plot = data['lang']
    extracted_info = data_to_plot.value_counts()    # return value and frequency of the value

    labels = []
    value = []
    
    for i, v in extracted_info.items():
        labels.append(i)
        value.append(v)
    
    nlpm.create_pie_chart(labels, value)
    
def plot_all(my_array, data):

    # plotting word_cloud in a matrix msl X msl,   msl = matrix_side_len

    t = 0
    matrix_side_len = len(my_array)
    matrix_side_len = int( math.ceil(math.sqrt( matrix_side_len) ) ) + 1
    for elem in my_array: 

        text = " ".join(chunk for chunk in elem if chunk)

        wordcloud = WordCloud(background_color="white", max_words=30).generate(text)
        i=t+1
        plt.subplot(matrix_side_len, matrix_side_len, i)
        plt.imshow(wordcloud)
        plt.axis("off")
        t += 1
    #plt.show()


    # creating pie_chart

    data_to_plot = data['lang']
    extracted_info = data_to_plot.value_counts()    # return value and frequency of the value

    labels = []
    value = []
    
    for i, v in extracted_info.items():
        labels.append(i)
        value.append(v)

    plt.plot()
    plt.pie(value, labels=labels)

    plt.show()


def plot_wordcloud(my_array):
    t = 0
    matrix_side_len = len(my_array)

    matrix_side_len = int( math.ceil(math.sqrt( matrix_side_len) ) )    # formula for have the length l*l = len(my_array)
    for text in my_array: 
        wordcloud = WordCloud(background_color="white", max_words=30).generate(text)
        i=t+1
        plt.subplot(matrix_side_len, matrix_side_len, i)
        plt.imshow(wordcloud)
        plt.axis("off")
        t += 1
    plt.show()




def main():

    start_time = time.time()

    iterate_on_folders(USE_DIRECTORY)

    end_time = time.time() 
    total_time = end_time - start_time

    print(total_time)
    

    print("\ntotal html file examinated: " + str(HTML_EXAMINATED))
    print("total folder scanned: " + str(FOLDER_SCANNED))
    print("total file scanned: " + str(TOTAL_FILE_SCANNED))
    print("total json claim reviewed found: " + str(TOTAL_CLAIM_REVIEW_FILE))


    dataset = create_dataset(html_array)
    create_csv(dataset)
    

    start_plot_time = time.time()

    
    #print(keywords_array)
    #print(len(keywords_array))
    plot_all(keywords_array, dataset)

    actual_time = time.time()
    plot_time = actual_time- start_plot_time

    print(plot_time)
    print(actual_time)

    actual_time = time.time()

    n_topics, lda_dict, lda_term_matrix = lda.lda(keywords_array)
    lda.plot_word_cloud(n_topics, lda_term_matrix, lda_dict)

main()


