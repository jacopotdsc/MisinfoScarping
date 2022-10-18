import collections
from distutils import text_file
from tkinter import SW
from typing import final
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS
from deep_translator import GoogleTranslator

# main text is in <p> tag and between
# <div class="edgtf-post-text-main"> e
# <div class="edgtf-post-info-bottom clearfix">


START_MAIN_TEXT = "<div class=\"edgtf-post-text-main\">"
END_MAIN_TEXT   = "<div class=\"edgtf-post-info-bottom clearfix\">"
HTML_TEXT_TAG   = "<p>"
HTML_WORDS      = ["<p>", "<a href", ">", "<", "/", "href", "https", "="]

MY_STOPSORDS = STOPWORDS

# True if there is html word, else False
def check_if_contain_html_words_or_stopwords(word):
    
    for w in HTML_WORDS:
        if word.find(w) != -1:
            if w not in HTML_WORDS:
                print("-- found HTML_WORD" + w + " in " + word)
            return True
    
    for sw in STOPWORDS:
        if word.find(sw) != -1:
            if sw not in STOPWORDS:
                print("-- found STOPWORDs" + sw + " in " + word)
            return True

    return False

# return array with all stopwords
def create_stopwords_set():
    all_stopwords = set()

    for sw in STOPWORDS:
        all_stopwords.add(sw)
    
    for w in HTML_WORDS:
        all_stopwords.add(w)
    return all_stopwords

# extract main text from html code
def extract_main_text(html_code):

    my_text = ''

    start_copy = False
    for line in html_code:

        if START_MAIN_TEXT in line:
            start_copy = True
        
        if END_MAIN_TEXT in line:
            start_copy = False
            break

        if start_copy == True and HTML_TEXT_TAG in line:
            my_text += translate_text(line)
            
    
    return my_text

# translate the main text of html page,  useful for STOPWORD provided by library
def translate_text(text):

    splitted_text = text.split("<p>")   # I need to split because is too long for translator
    final_translated_text = ''
    
    #print("entro, len: " + str(len(splitted_text)) )

    for i in range( len(splitted_text) ):

        sub_text = splitted_text[i]
        '''
        print(sub_text)
        print("subtext: " + str( len( sub_text)) )
        print()
        '''

        if(len(sub_text) > 4000 ):      # max text lenght for translator
            
            print("testo troppo lungo, riduco: " + str( len(sub_text) ) )

            step = 3000  # how much to increment
            start_index_string = 0
            final_index_string = step

            # I stop when I iterate all over the string
            while(start_index_string < len(sub_text)):

                substring_to_translate = sub_text[start_index_string, final_index_string]
                final_translated_text += GoogleTranslator(source='auto', target='en').translate(substring_to_translate)

                start_index_string += step
                final_index_string += step
    
        else:
            #print("translate ok, len: " + str(len(sub_text)))
            final_translated_text += GoogleTranslator(source='auto', target='en').translate(sub_text)
    
    return final_translated_text

def extract_keywords(html_file, max_common_words = 10):
    html_code = open(html_file,'r',errors="ignore")


    all_headlines = extract_main_text(html_code)
    #print(all_headlines_it)
    #all_headlines = translate_text(all_headlines_it[:3000])
    #all_headlines = translate_text(all_headlines_it)
    #print("translated")
    #print(all_headlines)

    stopwords = create_stopwords_set()
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(all_headlines[0:400])

    rcParams['figure.figsize'] = 5, 10
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.show()

    # this array will contain all words on the text
    filtered_words = [word for word in all_headlines.split() if word not in stopwords and check_if_contain_html_words_or_stopwords(word) == False ]
    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(max_common_words):
        words.append(letter)
        counts.append(count)

    colors = cm.rainbow(np.linspace(0, 1, 10))
    rcParams['figure.figsize'] = 10, 5
    plt.title('Top words in the headlines vs their count')
    plt.xlabel('Count')
    plt.ylabel('Words')
    plt.barh(words, counts, color=colors)
    #plt.show()

    return words



file1 = extract_keywords("gasdotto.html")
file2 = extract_keywords("confine_russia_finlandia.html")

print(file1)
print(file2)