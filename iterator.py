from msilib.schema import Directory
import os
from pickle import GLOBAL
from tkinter.tix import DirList
import html_check as hc
from time import sleep


#### GLOBAL VARIABLE
GLOBAL_DIRECTORY1 = "C:\\Users\\pc\\Desktop\\dataset thesys project" 
GLOBAL_DIRECTORY2 = "C:\\My Web Sites\\factanews\\facta.news" 
GLOBAL_DIRECTORY3 = "C:\\My Web Sites\\factanews"
GLOBAL_DIRECTORY4 = "C:\\misinfo"    # biggest folder: error

# set this variabile to choose to path to analize
USE_DIRECTORY = GLOBAL_DIRECTORY4

AUXLIARY_FOR_FORMAT = 0
HTML_EXAMINATED = 0

def increment_html_examinated():
    global HTML_EXAMINATED
    global AUXLIARY_FOR_FORMAT

    HTML_EXAMINATED = HTML_EXAMINATED + 1
    AUXLIARY_FOR_FORMAT = AUXLIARY_FOR_FORMAT + 1

    if AUXLIARY_FOR_FORMAT % 1000 == 0:
        print("-- html file examinated until now: " + str(HTML_EXAMINATED)) 
        sleep(0.5)


html_array = []

def iterate_on_folders(directory):

    dir_list = os.listdir(directory)
    for filename in dir_list:

        # analize html
        if filename.endswith(".html"):  
           result = hc.get_json(filename)
           html_array.append(result)

           increment_html_examinated()


        elif str(filename).find(".") != 1: # file extension have one ".", it is correct? 
            new_path = str(directory) + "\\" + filename
            #print(new_path)

            try:
                iterate_on_folders(new_path)
            except:
                continue
    

def create_csv(data_array):
    print("--- creating csv ---")

    if len(data_array) == 0:
        print("--- NO DATA COLLECTED ---")
        return


    my_file = open("data.csv","w", encoding="utf-8")

    #   I prepare file as a csv
    my_file.write("json,lang\n")

    for data in data_array:

        for j in data[0]:
            my_file.write(str(j) + "," + data[1])
        my_file.write("\n")

    my_file.close()


iterate_on_folders(USE_DIRECTORY)
#hc.html_array_print(html_array)
create_csv(html_array)
print("\ntotal html file examinated: " + str(HTML_EXAMINATED))