import collections
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud, STOPWORDS

#STOPWORDS = ["ciao", "ok"]
'''
STOPWORDS = ["type='text/css'", "media='all'/>", '<div',
 '</div>', '<a', '<script', "type='text/javascript'", '<link', 'di', '<meta', "relel='stylesheet'", '<span',
 "rel='stylesheet'", 'il', '</a>', 'a', 'che', '-->', 'in', 'la', '<!--', 'and',
 'target="_blank">', 'class="menu-item',
 'menu-item-type-post_type', 'menu-item-object-page',
 'style="color:', 'class="edgtf-social-icon-widget',
 '</div></figure>',
 'wp-block-embed-twitter"><div', 'class="wp-block-embed__wrapper">', '<blockquote', 'class="twitter-tweet"', 'data-width="550"', 
 'data-dnt="true"><p', '2022</a></blockquote><script',
 'src="../../../../../../platform.twitter.com/widgets.js"', 'charset="utf-8"></script>',
 '<figure', 'class="wp-block-embed',
 'type="application/rss+xml"',
 '.edgtf-layout1-item', '.edgtf-post-title', '.sd-content',
 'async', 'itemprop="url"', 'narrow"><a', 'class=""><span', 'class="item_outer"><span', 'class="widget',
 'rel="alternate"', 'var',
 '<li', 'class="edgtf-social-icon-widget-holder', 'edgtf-icon-has-hover"', 'data-hover-color="#dd3333"',
 '10px', 'aria-hidden="true"', 'class="edgtf-icon-font-elegant', '<input', 
'type="text"', 'class="edgtf-vertical-align-containers">', 'itemprop="image"', '<ul', '">',
"rel='dns-prefetch'", 'ul', '<img',
'//]]></script>',
'#262626;;font-size:', '20px"', 'title="Facta', '.post-excerpt', 'class="edgtf-grid">', '</span>',
'"><a', 'class="edgtf-column-content', 'edgtf-grid-col-4">', 'data-phone="393421829843"', 'href="javascript:void(0);"',
'name="google-site-verification"', 'alt=""', 'is-type-rich', 'is-provider-twitter', '</a>',
'target="_blank"', 'clearfix">',
'rel="icon"', '.edgtf-layout4-item', '.edgtf-ni-content', 'top,#fce434', 'figure', 'calc(.2em', '+', 'Global', 
'tag', '(gtag.js)', 'Google', 'Analytics', '<script>window.dataLayer=window.dataLayer||[];function', 
"gtag(){dataLayer.push(arguments);}gtag('js',new", 'href="javascript:void(0)">', '"></span>', 'type="submit"', 
'<header', 'href="../../../../../index.html"', 'style="height:', 'class="edgtf-position-center">', 
'class="edgtf-position-center-inner">', '<nav', 'href="../../../../../chi-siamo/index.html"', 
'href="../../../../../antibufale/index.html"', 'href="../../../../../storie/index.html"', 'href="../../../../index.html"', 
'href="../../../../../segnalazioni/index.html"', 'href="../../../../../veramente-il-podcast-di-facta-news/index.html"', 
'class="edgtf-position-right">', 'class="edgtf-position-right-inner">', 'name="generator"', 'fa-linkedin"></span>',
'</p>', 'href'

]
'''

HTML_WORDS = [  "<", ">", "href", "id", "src", "script", "class", 
                "=", "header", "edgtf", "gtag", "sd-content", "<!--", 
                "-->", "Copier/", "font-size",
                "tag", "div", "px", "widget", "media", "noscript", "style",
                "rel", "async", "format", "size-full", "noreferrer", "sd-button",
                "Font", "wbr", "video", "var", "ul", "<time>", "<textarea", "tbody", "sup",
                "<source", "type", "Stream", "object"
            ]


# True if there is html word, else False
def check_if_contain_html_words_or_stopwords(word):
    
    for w in HTML_WORDS:
        if word.find(w) != -1:
            if w not in HTML_WORDS:
                print("-- found " + w + " in " + word)
            return True
    
    for sw in STOPWORDS:
        if word.find(sw) != -1:
            if sw not in STOPWORDS:
                print("-- found " + w + " in " + word)
            return True

    return False

html_code = open("gasdotto.html",'r',errors="ignore")


all_headlines = ''

for line in html_code:
    all_headlines += line


stopwords = STOPWORDS
wordcloud = WordCloud(stopwords=stopwords, background_color="white", max_words=1000).generate(all_headlines)

rcParams['figure.figsize'] = 10, 20
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

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