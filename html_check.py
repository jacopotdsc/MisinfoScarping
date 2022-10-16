from array import array
from fileinput import filename
from bs4 import BeautifulSoup
import urllib
import re
import json
from textblob import TextBlob # NOT USED
import langid # NOT USED


##### VARIABLE DEBUG #####
KEYWORD_FOUND_DEBUG = False   # used for print keyword found. to understand why a json is extracted
PRINT_ERROR_READY_HTML = False # show what filemy program wasn't able to open

##### COSTANT VARIABLE #####

# words that can charaterize json ClaimReview which I'd like to find
MAIN_KEYWORD = ["Generated by Full Fact Claim Review Schema"]
CLAIM_JSON_KEYWORD = [ "claimReviewed", "itemReviewed", "reviewRating" ]
JSON_KEYWORD = ["script type=\"application/ld+json\""]
LANG_KEYWORD = ["html lang"]
#JSON_KEYWORD = ["ciaoo"]

##### GLOBAL VARIABLE #####




##### FUNCTION TO CHECK FOR JSON #####

# extrace language of page
def extract_language(line):
  
  # model's line: <html lang="it-IT">

  text1 = line.split("lang=")   
  text2 = text1[1].split(">")

  return text2[0]

# give line which contain json file, return a json object
def convert_string_to_json(line):

  # line scheme: [<script ..>{json}</script>]
  
  text1 = line.split(">")
  text2 = text1[1].split("<")

  return json.loads(text2[0])

# check if it's present a json with CLAIM_JSON_KEYWORD  
def check_if_is_json(my_json, keyword_list, line):

  json_found = False

  for keyword in keyword_list:

      if json_found == False and line.find(keyword) != -1:

        if KEYWORD_FOUND_DEBUG == True: print("found with " + keyword)

        obj_json = convert_string_to_json( line )
        my_json.append( obj_json )

        json_found = True

      # to avoid some iteration, I force loop to stop
      if json_found == True:
        break

  return json_found


#### MODIFICARE L'ORDINE, DAL PIU PROBABILE AL MENO PROBABILE
#### LEVARE IL BREAK, PERCHè MAGARI CI SONO DEI CASI IN CUI NON
#### SCANNERIZZA MAI QUELLO PER LA LINGUA
#### AGGIUNGERE UNA VARIABILE DI CHECK PER EVITARE CIò

# take all possible claimReviewed scheme
def get_claimReviewed_scheme_in_html_code(file_name):


  html_code = ''
  try:
    html_code = open(file_name,'r',errors="ignore")
  except:
    if  PRINT_ERROR_READY_HTML == True:
      print("html_check.get_claimReviewed_scheme_in_html_code(file_name) -> error to open: " + str(filename) )
  
  #html_code = open(file_name,'r',errors="ignore")

  # loop on each line of the code, to find a possible claimReviewed scheme
  my_json = []
  language = ''
  for line in html_code:

    # check if CLAIM_JSON_KEYWORD
    claim_json_keyword_result = check_if_is_json(my_json, CLAIM_JSON_KEYWORD, line)
    if claim_json_keyword_result == True:
      break

    # check if JSON_KEYWORD
    json_keyword_result = check_if_is_json(my_json, JSON_KEYWORD, line)
    if json_keyword_result == True:
      break

     # check if MAIN_KEYWORD
    main_keyword_result = check_if_is_json(my_json, MAIN_KEYWORD, line)
    if main_keyword_result == True:
      break

    # language of the page
    if line.find(LANG_KEYWORD[0]) != -1:
        language = extract_language(line)
        continue
  
  return (my_json, language)


# Take an array with entry < json_file, language > given by get_claimReviewed_scheme_in_html_code(file_name)
def html_array_print(html_array):

  # r-tuple: < json_list, language >, can be present more than one json!
  for r in html_array:
    json_list = r[0]
    language = r[1]

    if json_list== []:
      print("--- no json found ---")

    else:
      print("\n----- result -----")
      print("language: " + language)

      for j in json_list:
        print("my_json: " + str( type( j ) ) )
        print(j)
    

# return a pair < json_file, language >
def get_json(filename_array, print_result = False):

  html_file = []
  for f in filename_array:
    result = get_claimReviewed_scheme_in_html_code(f)
    html_file.append(result)
  
  if print_result == True:
    html_array_print(html_file)

  return html_file




'''
result1 = get_claimReviewed_scheme_in_html_code("gasdotto.html")
result2 = get_claimReviewed_scheme_in_html_code("confine_russia_finlandia.html")

result = []
result.append(result1)
result.append(result2)

#html_array_print(result)

name_array = ["gasdotto.html", "confine_russia_finlandia.html"]
get_json(name_array, True)
'''