import collections
from distutils import text_file
from fnmatch import translate
from tkinter import SW
from typing import final
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS
from deep_translator import GoogleTranslator
import time
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

# main text is in <p> tag and between
# <div class="edgtf-post-text-main"> e
# <div class="edgtf-post-info-bottom clearfix">


START_MAIN_TEXT = "<div class=\"edgtf-post-text-main\">"
END_MAIN_TEXT   = "<div class=\"edgtf-post-info-bottom clearfix\">"
HTML_TEXT_TAG   = "<p>"
HTML_WORDS      = ["<a", "<p>", "<a href", ">", "<", "/", "href", "https", "=", "target=", "rel=" ]



# True if there is html word or stopwords, else False
def check_if_contain_html_words_or_stopwords(word, my_stopwords):
    
    for sw in my_stopwords:
        ##if word.find(sw) != -1:
        if word.lower() == sw.lower():  # to make them equals
            return True
    
    return False

# return an array with all ulr in the main text
def extract_all_url(main_text):
    #soup = BeautifulSoup(main_text)
    soup = BeautifulSoup(main_text, features="html5lib")  

    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    return links

# extract main text from html code
def extract_main_text(html_code):


    # extract ONLY the main text, the main body
    my_text = ''

    start_copy = False
    for line in html_code:

        if START_MAIN_TEXT in line:
            start_copy = True
        
        if END_MAIN_TEXT in line:
            start_copy = False
            break

        if start_copy == True and HTML_TEXT_TAG in line:
            my_text += line


    return my_text

# take html_main_text and return text without html tags
def clear_html_text(text_to_clear):

    soup = BeautifulSoup(text_to_clear, features="html.parser")
    
    for script in soup(["scipt", "style"]):
        script.extract()       # rip out all thing which I don't need

    text = soup.get_text()
    #print(text)

    lines = (line.strip() for line in text.splitlines())

    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


# create and show a pie-char given data and their labels 
def create_pie_chart(my_labels, data):

    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels=my_labels)
 
    # show plot
    plt.show()


def get_stopwords(language):
  return stopwords.words(language)


def extract_informations(html_file, max_common_words = 15, language='italian'):

   # print("-- opening path: " + html_file)
    html_code = open(html_file,'r',errors="ignore", encoding='UTF-8')


    main_text_html_version = extract_main_text(html_code)
    all_url = extract_all_url(main_text_html_version)
    main_text = clear_html_text(main_text_html_version)


    my_stopwords = list( stopwords.words(language) )
    wordcloud = WordCloud(stopwords=my_stopwords, background_color="white", max_words=20).generate(main_text)

    #print(type(wordcloud))
    #print(all_headlines)

    '''
    rcParams['figure.figsize'] = 5, 10
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    '''

    # this array will contain all words on the text
    filtered_words = [word for word in main_text.split() if word not in my_stopwords and check_if_contain_html_words_or_stopwords(word, my_stopwords) == False ]# and word.isnumeric() == False ]

    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(max_common_words):
        words.append(letter)
        counts.append(count)
        #print(letter + " -> " + str(count) )

    '''
    colors = cm.rainbow(np.linspace(0, 1, 10))
    rcParams['figure.figsize'] = 10, 5
    plt.title('Top words in the headlines vs their count')
    plt.xlabel('Count')
    plt.ylabel('Words')
    plt.barh(words, counts, color=colors)
    plt.show()
    '''

    return words, all_url

'''
file1 = extract_informations("try_folder_scan\\gasdotto.html")
file2 = extract_informations("try_folder_scan\\incendio_auto.html")

print(file1)
print(file2)
'''






