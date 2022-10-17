import collections
from tkinter import SW
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS

# main text is in <p> tag and between
# <div class="edgtf-post-text-main"> e
# <div class="edgtf-post-info-bottom clearfix">


START_MAIN_TEXT = "<div class=\"edgtf-post-text-main\">"
END_MAIN_TEXT   = "<div class=\"edgtf-post-info-bottom clearfix\">"
HTML_TEXT_TAG   = "<p>"
HTML_WORDS      = ["<p>", "<a href", ">", "<", "/", "href", "https"]

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
            my_text += line
    
    return my_text


def extract_keywords(html_file):
    html_code = open(html_file,'r',errors="ignore")


    all_headlines = extract_main_text(html_code)

    print(all_headlines)

    stopwords = create_stopwords_set()
    wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(all_headlines)

    rcParams['figure.figsize'] = 10, 20
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

    # this array will contain all words on the text
    filtered_words = [word for word in all_headlines.split() if word not in stopwords and check_if_contain_html_words_or_stopwords(word) == False ]
    counted_words = collections.Counter(filtered_words)
    words = []
    counts = []
    for letter, count in counted_words.most_common(20):
        words.append(letter)
        counts.append(count)

    print(words)
    colors = cm.rainbow(np.linspace(0, 1, 10))
    rcParams['figure.figsize'] = 20, 10
    plt.title('Top words in the headlines vs their count')
    plt.xlabel('Count')
    plt.ylabel('Words')
    plt.barh(words, counts, color=colors)
    plt.show()

    return words



file1 = extract_keywords("gasdotto.html")
file2 = extract_keywords("confine_russia_finlandia.html")

print(file1)
print(file2)