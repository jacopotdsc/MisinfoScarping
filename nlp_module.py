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
LANGUAGE_CODE   = {'ab': "'Abkhaz'", 'ae': "'Avestan'", 'af': "'Afrikaans'", 'ak': "'Akan'", 'am': "'Amharic'", 'an': "'Aragonese'", 'ar': "'Arabic'", 'as': "'Assamese'", 'av': "'Avaric'", 'ay': "'Aymara'", 'az': 
"'Azerbaijani'", 'ba': "'Bashkir'", 'be': "'Belarusian'", 'bg': "'Bulgarian'", 'bi': "'Bislama'", 'bm': "'Bambara'", 'bn': "'Bengali'", 'bo': "'Tibetan'", 'br': "'Breton'", 'bs': "'Bosnian'", 'ca': "'Catalan'", 'ce': "'Chechen'", 'ch': "'Chamorro'", 'co': "'Corsican'", 'cr': "'Cree'", 'cs': "'Czech'", 'cu': "'Old", 'cv': "'Chuvash'", 'cy': "'Welsh'", 'da': "'Danish'", 'de': "'German'", 'dv': "'Divehi'", 'dz': "'Dzongkha'", 'ee': "'Ewe'", 'el': "'Greek'", 'en': "'English'", 'eo': "'Esperanto'", 'es': "'Spanish'", 'et': "'Estonian'", 'eu': "'Basque'", 'fa': "'Persian'", 'ff': "'Fula'", 'fi': "'Finnish'", 'fj': "'Fijian'", 'fo': "'Faroese'", 'fr': "'French'", 'fy': "'Western", 'ga': "'Irish'", 'gd': "'Scottish", 'gl': "'Galician'", 'gn': "'Guaraní'", 'gu': "'Gujarati'", 'gv': "'Manx'", 'ha': "'Hausa'", 'he': "'Hebrew'", 'hi': "'Hindi'", 'ho': "'Hiri", 'hr': "'Croatian'", 'ht': "'Haitian'", 'hu': "'Hungarian'", 'hy': "'Armenian'", 'hz': "'Herero'", 'ia': "'Interlingua'", 'id': "'Indonesian'", 'ie': "'Interlingue'", 'ig': "'Igbo'", 'ii': "'Nuosu'", 'ik': "'Inupiaq'", 'io': "'Ido'", 'is': "'Icelandic'", 'it': "'Italian'", 'iu': "'Inuktitut'", 'ja': "'Japanese'", 'jv': "'Javanese'", 'ka': "'Georgian'", 'kg': "'Kongo'", 'ki': "'Kikuyu'", 'kj': "'Kwanyama'", 'kk': "'Kazakh'", 'kl': "'Kalaallisut'", 'km': "'Khmer'", 'kn': "'Kannada'", 'ko': "'Korean'", 
'kr': "'Kanuri'", 'ks': "'Kashmiri'", 'ku': "'Kurdish'", 'kv': "'Komi'", 'kw': "'Cornish'", 'ky': "'Kyrgyz'", 'la': "'Latin'", 'lb': "'Luxembourgish'", 'lg': "'Ganda'", 'li': "'Limburgish'", 'ln': "'Lingala'", 'lo': "'Lao'", 'lt': "'Lithuanian'", 'lu': "'Luba-Katanga'", 'lv': "'Latvian'", 'mg': "'Malagasy'", 'mh': "'Marshallese'", 'mi': "'Māori'", 'mk': "'Macedonian'", 'ml': "'Malayalam'", 'mn': "'Mongolian'", 'mr': "'Marathi'", 'ms': "'Malay'", 'mt': "'Maltese'", 'my': "'Burmese'", 'na': "'Nauru'", 'nb': "'Norwegian", 'nd': "'Northern", 'ne': "'Nepali'", 'ng': "'Ndonga'", 'nl': "'Dutch'", 'nn': "'Norwegian", 'no': "'Norwegian'", 'nr': "'Southern", 'nv': "'Navajo'", 'ny': "'Chichewa'", 'oc': "'Occitan'", 'oj': "'Ojibwe'", 'om': "'Oromo'", 'or': "'Oriya'", 'os': "'Ossetian'", 'pa': "'Panjabi'", 'pi': "'Pāli'", 'pl': "'Polish'", 'ps': "'Pashto'", 'pt': "'Portuguese'", 'qu': "'Quechua'", 'rm': "'Romansh'", 'rn': "'Kirundi'", 'ro': "'Romanian'", 'ru': "'Russian'", 
'rw': "'Kinyarwanda'", 'sa': "'Sanskrit'", 'sc': "'Sardinian'", 'sd': "'Sindhi'", 'se': "'Northern", 'sg': "'Sango'", 'si': "'Sinhala'", 'sk': "'Slovak'", 'sl': "'Slovenian'", 'sm': "'Samoan'", 'sn': "'Shona'", 'so': "'Somali'", 'sq': "'Albanian'", 'sr': "'Serbian'", 'ss': "'Swati'", 'st': "'Southern", 'su': "'Sundanese'", 'sv': "'Swedish'", 'sw': "'Swahili'", 'ta': "'Tamil'", 'te': "'Telugu'", 'tg': "'Tajik'", 'th': "'Thai'", 'ti': "'Tigrinya'", 'tk': "'Turkmen'", 'tl': "'Tagalog'", 'tn': "'Tswana'", 'to': "'Tonga'", 'tr': "'Turkish'", 'ts': "'Tsonga'", 'tt': "'Tatar'", 'tw': "'Twi'", 'ty': "'Tahitian'", 'ug': "'Uyghur'", 'uk': "'Ukrainian'", 'ur': "'Urdu'", 'uz': "'Uzbek'", 've': "'Venda'", 'vi': "'Vietnamese'", 'vo': "'Volapük'", 'wa': "'Walloon'", 'wo': "'Wolof'", 'xh': "'Xhosa'", 'yi': "'Yiddish'", 'yo': "'Yoruba'", 'za': "'Zhuang'", 'zh': "'Chinese'", 'zu': "'Zulu'"}



# True if there are stopwords, else False
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

    #soup = BeautifulSoup(text_to_clear, features="html.parser")
    soup = BeautifulSoup(text_to_clear, features="html5lib")  

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

# return an array with all stopwords of the language
def get_stopwords(language):
  return stopwords.words(language)

# return keywords of the text and all url inside the main text
def extract_informations(html_file, max_common_words = 15, language='italian'):

   # print("-- opening path: " + html_file)
    html_code = open(html_file,'r',errors="ignore", encoding="UTF-8")


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






