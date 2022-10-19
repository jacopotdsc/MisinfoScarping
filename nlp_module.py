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

MY_STOPSORDS_EN = STOPWORDS
#MY_STOPSORDS_IT = ['avere', 'stato', 'sei', 'non potevo', 'di', 'Appena', 'fuori', 'tutto', 'il', 'voluto', 'non', 'non deve', 'sono', 'ottenere', 'io sono', 'questo', 'io', 'non lo farebbe', 'non lo sono', 'Fino a', 'fatto', 'no', 'però', 'una volta', 'il vostro', 'Sopra', 'capannone', 'andiamo', 'anche', 'lui stesso', 'tale', 'lo farai', 'me', 'id', 'loro stessi', 'non lo erano', 'pochi', 'erano', "cos'è", 'la sua', 'quindi', 'sopra', 'o', 'mio', 'fra', 'dopo', 'quando è', 'me stesso', 'in occasione', 'insieme a', 'quale', 'ecco', 'K', 'spento', 'suo', 'loro', 'com', 'è', 'ulteriore', 'lo faresti', 'non lo fa', 'se stessa', 'in', 'non posso', 'là', 'a', 'come', 'Su', 'ha', 'Se', 'lei', 'stesso', 'lo faremmo', 'non', 'fuori uso', 'non farlo', 'solo', 'noi stessi', 'e', 'mentre', 'avendo', 'ma', 'lui', 'quello è', 'perché', 'Quello', 'il suo', 'perché', 'in', 'essi', 'lei è', 'malato', 'noi', 'chi', 'non ho', 'per', 'altro', 'Entrambi', 'dove', 'non dovrebbe', 'essere', 'facendo', 'mai', 'queste', 'poi', 'noi abbiamo', 'quando', 'r', 'non ha', 'altrimenti', 'a testa', 'sotto', 'www', 'lo faranno', 'lui è', 'non lo è', 'hanno', 'un', "dov 'è", 'di', "c'è", 'http', 'si', 'quelli', 'anche', 'sotto', 'contro', 'come', 'Così', 'molto', 'che cosa', 'io ho', 'te stesso', 'lui', 'chi è', 'qui', 'i nostri', 'qualunque', 'Potere', 'più', 'non lo era', 'a', 'non', 'sono', 'bene', 'essendo', 'piace', 'hai', 'tuo', 'fa', 'non aveva', 'Potevo', 'di', "com'è", 'esso', 'su', 'fare', 'era', 'Loro sono', 'ancora', 'prima', 'non può', 'lo avrebbero fatto', 'un', 'voi stessi', 'da', 'da', 'inferno', 'nostro', 'Di più', 'deve', 'dunque', 'dovrebbe', 'di', 'il loro', 'guscio', 'Altro', 'No', 'perché', 'dovrebbe', 'possedere', 'né', 'voi', 'è', 'erano', 'chi', 'lui', 'suo', 'alcuni', 'attraverso', 'i loro', 'avevo']
MY_STOPSORDS_IT = ['nel','del', 'le', 'con', 'dalla', 'il', 'dal', 'al', 'la', 
                    'che', 'avere', 'stato', 'sei', 'non potevo', 'di', 'Appena', 
                    'fuori', 'tutto', 'il', 'voluto', 'non', 'non deve', 'sono', 
                    'ottenere', 'io sono', 'questo', 'io', 'non lo farebbe', 'non lo sono', 
                    'Fino a', 'fatto', 'no', 'però', 'una volta', 'il vostro', 'Sopra', 
                    'capannone', 'andiamo', 'anche', 'lui stesso', 'tale', 'lo farai', 
                    'me', 'id', 'loro stessi', 'non lo erano', 'pochi', 'erano', "cos'è", 
                    'la sua', 'quindi', 'sopra', 'o', 'mio', 'fra', 'dopo', 'quando è', 
                    'me stesso', 'in occasione', 'insieme a', 'quale', 'ecco', 'K', 
                    'spento', 'suo', 'loro', 'com', 'è', 'ulteriore', 'lo faresti', 'non lo fa', 
                    'se stessa', 'in', 'non posso', 'là', 'a', 'come', 'Su', 'ha', 'Se', 
                    'lei', 'stesso', 'lo faremmo', 'non', 'fuori uso', 'non farlo', 
                    'solo', 'noi stessi', 'e', 'mentre', 'avendo', 'ma', 'lui', 'quello è', 
                    'perché', 'Quello', 'il suo', 'perché', 'in', 'essi', 'lei è', 'malato', 
                    'noi', 'chi', 'non ho', 'per', 'altro', 'Entrambi', 'dove', 'non dovrebbe', 
                    'essere', 'facendo', 'mai', 'queste', 'poi', 'noi abbiamo', 'quando', 'r', 
                    'non ha', 'altrimenti', 'a testa', 'sotto', 'www', 'lo faranno', 'lui è', 'non lo è',
                     'hanno', 'un', "dov 'è", 'di', "c'è", 'http', 'si', 'quelli', 'anche', 'sotto', 
                     'contro', 'come', 'Così', 'molto', 'che cosa', 'io ho', 'te stesso', 'lui', 'chi è', 
                     'qui', 'i nostri', 'qualunque', 'Potere', 'più', 'non lo era', 'a', 'non', 'sono', 
                     'bene', 'essendo', 'piace', 'hai', 'tuo', 'fa', 'non aveva', 'Potevo', 'di', "com'è", 
                     'esso', 'su', 'fare', 'era', 'Loro sono', 'ancora', 'prima', 'non può', 'lo avrebbero fatto', 
                     'un', 'voi stessi', 'da', 'da', 'inferno', 'nostro', 'Di più', 'deve', 'dunque', 'dovrebbe', 
                     'di', 'il loro', 'guscio', 'Altro', 'No', 'perché', 'dovrebbe', 'possedere', 'né', 'voi', 'è',
                      'erano', 'chi', 'lui', 'suo', 'alcuni', 'attraverso', 'i loro', 'avevo'
                      
                    ]



my_stowords_dict = {'it': MY_STOPSORDS_IT, 'en': MY_STOPSORDS_EN}

# True if there is html word or stopwords, else False
def check_if_contain_html_words_or_stopwords(word, my_stopwords):
    
    for sw in my_stopwords:
        ##if word.find(sw) != -1:
        if word.lower() == sw.lower():  # to make them equals
            return True
    
    return False

# return array with all stopwords
def create_stopwords_set():
    all_stopwords = set()

    for k in my_stowords_dict:
        for word in my_stowords_dict[k]:
            all_stopwords.add(word)
    
    for w in HTML_WORDS:
        all_stopwords.add(w)
    return all_stopwords


# return an array with all ulr in the main text
def extract_all_url(main_text):
    soup = BeautifulSoup(main_text)

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

# translate the main text of html page,  useful for STOPWORD provided by library
def translate_html_text(text):

    splitted_text = text.split("<p>")   # I need to split because is too long for translator
    final_translated_text = ''

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
    html_code = open(html_file,'r',errors="ignore", encoding='UTF-8')


    main_text_html_version = extract_main_text(html_code)
    all_url = extract_all_url(main_text_html_version)
    main_text = clear_html_text(main_text_html_version)

    print("number of ulr: " + str(len(all_url)))

    my_stopwords = list( stopwords.words('italian') )
    print("ecco le stopwords")
    print(type(my_stopwords[0]))
    wordcloud = WordCloud(stopwords=my_stopwords, background_color="white", max_words=1000).generate(main_text[0:400])

    #print(all_headlines)

    rcParams['figure.figsize'] = 5, 10
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.show()

    # this array will contain all words on the text
    filtered_words = [word for word in main_text.split() if word not in my_stopwords and check_if_contain_html_words_or_stopwords(word, my_stopwords) == False ]# and word.isnumeric() == False ]
    #filtered_words = [word for word in all_headlines.split() if word not in my_stopwords and check_if_contain_html_words_or_stopwords(word, my_stopwords) == False and word.isnumeric() == False ]
    
    #filtered_words = [word for word in all_headlines.split() if word not in stopwords]

    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(max_common_words):
        words.append(letter)
        counts.append(count)
        print(letter + " -> " + str(count) )

    colors = cm.rainbow(np.linspace(0, 1, 10))
    rcParams['figure.figsize'] = 10, 5
    plt.title('Top words in the headlines vs their count')
    plt.xlabel('Count')
    plt.ylabel('Words')
    plt.barh(words, counts, color=colors)
    #plt.show()

    return words



#file1 = extract_keywords("gasdotto.html")
file2 = extract_keywords("try_folder_scan\\incendio_auto.html")

#print(file1)
print(file2)


'''
text = '<p>La mattina del 21 settembre Vladimir Putin <a href="http://en.kremlin.ru/events/president/news/69390" target="_blank" rel="noreferrer noopener">ha annunciato</a> una â€œmobilitazione parzialeâ€ in Russia per reclutare nuovi soldati da mandare in guerra in Ucraina. Il presidente russo ha precisato che verranno coinvolti in primo luogo i riservisti militari, cioÃ¨ Â«coloro che hanno prestato servizio in precedenza nelle forze armateÂ».Â </p>'
link_clear = clear_from_url(text)
p_clear = clear_html_text(text)

print("---risultati---")
print(p_clear)
'''

