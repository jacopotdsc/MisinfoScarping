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

# main text is in <p> tag and between
# <div class="edgtf-post-text-main"> e
# <div class="edgtf-post-info-bottom clearfix">


START_MAIN_TEXT = "<div class=\"edgtf-post-text-main\">"
END_MAIN_TEXT   = "<div class=\"edgtf-post-info-bottom clearfix\">"
HTML_TEXT_TAG   = "<p>"
HTML_WORDS      = ["<p>", "<a href", ">", "<", "/", "href", "https", "="]

MY_STOPSORDS_EN = STOPWORDS
MY_STOPSORDS_IT = ['avere', 'stato', 'sei', 'non potevo', 'di', 'Appena', 'fuori', 'tutto', 'il', 'voluto', 'non', 'non deve', 'sono', 'ottenere', 'io sono', 'questo', 'io', 'non lo farebbe', 'non lo sono', 'Fino a', 'fatto', 'no', 'però', 'una volta', 'il vostro', 'Sopra', 'capannone', 'andiamo', 'anche', 'lui stesso', 'tale', 'lo farai', 'me', 'id', 'loro stessi', 'non lo erano', 'pochi', 'erano', "cos'è", 'la sua', 'quindi', 'sopra', 'o', 'mio', 'fra', 'dopo', 'quando è', 'me stesso', 'in occasione', 'insieme a', 'quale', 'ecco', 'K', 'spento', 'suo', 'loro', 'com', 'è', 'ulteriore', 'lo faresti', 'non lo fa', 'se stessa', 'in', 'non posso', 'là', 'a', 'come', 'Su', 'ha', 'Se', 'lei', 'stesso', 'lo faremmo', 'non', 'fuori uso', 'non farlo', 'solo', 'noi stessi', 'e', 'mentre', 'avendo', 'ma', 'lui', 'quello è', 'perché', 'Quello', 'il suo', 'perché', 'in', 'essi', 'lei è', 'malato', 'noi', 'chi', 'non ho', 'per', 'altro', 'Entrambi', 'dove', 'non dovrebbe', 'essere', 'facendo', 'mai', 'queste', 'poi', 'noi abbiamo', 'quando', 'r', 'non ha', 'altrimenti', 'a testa', 'sotto', 'www', 'lo faranno', 'lui è', 'non lo è', 'hanno', 'un', "dov 'è", 'di', "c'è", 'http', 'si', 'quelli', 'anche', 'sotto', 'contro', 'come', 'Così', 'molto', 'che cosa', 'io ho', 'te stesso', 'lui', 'chi è', 'qui', 'i nostri', 'qualunque', 'Potere', 'più', 'non lo era', 'a', 'non', 'sono', 'bene', 'essendo', 'piace', 'hai', 'tuo', 'fa', 'non aveva', 'Potevo', 'di', "com'è", 'esso', 'su', 'fare', 'era', 'Loro sono', 'ancora', 'prima', 'non può', 'lo avrebbero fatto', 'un', 'voi stessi', 'da', 'da', 'inferno', 'nostro', 'Di più', 'deve', 'dunque', 'dovrebbe', 'di', 'il loro', 'guscio', 'Altro', 'No', 'perché', 'dovrebbe', 'possedere', 'né', 'voi', 'è', 'erano', 'chi', 'lui', 'suo', 'alcuni', 'attraverso', 'i loro', 'avevo']

my_stowords_dict = {'it': MY_STOPSORDS_IT, 'en': MY_STOPSORDS_EN}

# True if there is html word, else False
def check_if_contain_html_words_or_stopwords(word, stopwords):
    
    for sw in stopwords:
        if word.find(sw) != -1:
            return True
    
    return False
    '''
    for w in HTML_WORDS:
        if word.find(w) != -1:
            if w not in HTML_WORDS:
                print("-- found HTML_WORD" + w + " in " + word)
            return True
    
    for sw in STOPWORDS:
        if word.find(sw) != -1:
            if sw not in STOPWORDS:
                print("-- found STOPWORDS" + sw + " in " + word)
            return True

    return False
    '''

# return array with all stopwords
def create_stopwords_set():
    all_stopwords = set()

    for k in my_stowords_dict:
        for word in my_stowords_dict[k]:
            all_stopwords.add(word)
    
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
            my_text += line
    
    return my_text

# translate the main text of html page,  useful for STOPWORD provided by library
def translate_html_text(text):

    splitted_text = text.split("<p>")   # I need to split because is too long for translator
    final_translated_text = ''
    
    #print("entro, len: " + str(len(splitted_text)) )

    for i in range( len(splitted_text) ):

        sub_text = splitted_text[i]

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

def translate_stopwords(array, s='auto', t='it'):
    translated_array = []

    for p in array:
        translated_word =  GoogleTranslator(source=s, target=t).translate(p)
        translated_array.append(p)
    
    return translated_array
    


def extract_keywords(html_file, max_common_words = 10):
    html_code = open(html_file,'r',errors="ignore")


    all_headlines = extract_main_text(html_code)
    #print(all_headlines_it)
    #all_headlines = translate_text(all_headlines_it[:3000])

    #print(all_headlines)

    stopwords = create_stopwords_set()
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(all_headlines[0:400])

    rcParams['figure.figsize'] = 5, 10
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.show()

    # this array will contain all words on the text
    filtered_words = [word for word in all_headlines.split() if word not in stopwords and check_if_contain_html_words_or_stopwords(word, stopwords) == False ]# and word.isnumeric() == False ]
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



start_time = time.time()
print(translate_stopwords(MY_STOPSORDS_EN))
print("--- %s seconds ---" % (time.time() - start_time))

file1 = extract_keywords("gasdotto.html")
file2 = extract_keywords("confine_russia_finlandia.html")

print(file1)
print(file2)