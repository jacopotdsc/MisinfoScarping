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
GLOBAL_DIRECTORY4 = "C:\\My Web Sites"
GLOBAL_DIRECTORY5 = "C:\\misinfo"    # biggest folder: error

# set this variabile to choose to path to analize
USE_DIRECTORY = GLOBAL_DIRECTORY2

#### VARIABLE STATUS SCANN ####
PRINT_SCAN_STATUS = False   # to print status of iteration
VAR_SLEEP = 0               # variabile to read print of scan
AUXLIARY_FOR_FORMAT = 0     # variable for print
HTML_EXAMINATED = 0         # counter for html examinated
FOLDER_SCANNED = 0          # counter for folder scanned
TOTAL_FILE_SCANNED = 0      # counter for total scan / iteration

def increment_total_file_scanned():
    global TOTAL_FILE_SCANNED
    
    TOTAL_FILE_SCANNED = TOTAL_FILE_SCANNED + 1

    if AUXLIARY_FOR_FORMAT % 1000 == 0 and AUXLIARY_FOR_FORMAT > 500:
        if PRINT_SCAN_STATUS == True:
            print("-- total file scanned until now: " + str(TOTAL_FILE_SCANNED))
            sleep(VAR_SLEEP)

def increment_html_examinated():
    global HTML_EXAMINATED
    global AUXLIARY_FOR_FORMAT

    HTML_EXAMINATED = HTML_EXAMINATED + 1
    AUXLIARY_FOR_FORMAT = AUXLIARY_FOR_FORMAT + 1

    if AUXLIARY_FOR_FORMAT % 1000 == 0:
        if PRINT_SCAN_STATUS == True:
            print("-- html file examinated until now: " + str(HTML_EXAMINATED)) 
            sleep(VAR_SLEEP)

def increment_folder_scannned():
    global FOLDER_SCANNED

    FOLDER_SCANNED = FOLDER_SCANNED + 1

    if AUXLIARY_FOR_FORMAT % 1000 == 0 and AUXLIARY_FOR_FORMAT > 500:
        if PRINT_SCAN_STATUS == True:
            print("-- total folder scanned until now: " + str(FOLDER_SCANNED))
            sleep(VAR_SLEEP)

html_array = []

def iterate_on_folders(directory):

    dir_list = os.listdir(directory)
    for filename in dir_list:

        increment_total_file_scanned()

        # analize html
        if filename.endswith(".html"):  
            result = hc.get_json([filename])

            # result is an array of < json_file, lang >
            for r in result:
                for file_json in r[0]:
                    new_json = file_json
                    new_json['lang'] = r[1]
                    html_array.append(new_json)

            increment_html_examinated()


        elif os.path.isdir(str(directory) + "\\" + filename) == True:
            new_path = str(directory) + "\\" + filename

            increment_folder_scannned()
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
        my_file.write(str(data) + "," + data['lang'] + "\n")

    my_file.close()


iterate_on_folders(USE_DIRECTORY)
#hc.html_array_print(html_array)
create_csv(html_array)
print("\ntotal html file examinated: " + str(HTML_EXAMINATED))
print("total folder scanned: " + str(FOLDER_SCANNED))
print("total file scanned: " + str(TOTAL_FILE_SCANNED))
#print(html_array)