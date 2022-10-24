from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
from wordcloud import WordCloud
import matplotlib as plt

keyword_array = [['Putin:', '“non', 'accetto', 'lezioni', 'democrazia', 'paese', 'impedisce', 'parte', 'popolazione', 'persino', 'prendere', 'l’autobus', 'andare', 'lavoro”'], ['auto', 'state', 'bruciate', 'rifugiati', 'ucraini', 'motivazioni', 'politiche', 'legate', 'guerra', 'Russia'], ['somministrando', 'mucche', 'vaccino', 'mRNA', 'passerà', 'vaccino', 'latte,', 'formaggio,', 'ecc'], ['foto', 'mostrano', 'folla', 'manifestazione', 'pro', 'Trump', '14', 'novembre', '2020'], ['Putin:', '“non', 'accetto', 'lezioni', 'democrazia', 'paese', 'impedisce', 'parte', 'popolazione', 'persino', 'prendere', 'l’autobus', 'andare', 'lavoro”'], ['video', 'luna', 'stato', 'girato', 'confine', 'Canada,', 'Alaska', 'Russia.', 'fenomeno', 'verifica', 'solo', 'perigeo', '(il', 'punto', 'luna', 'vicina', 'terra)', 'proprio', 'qui', 'possiamo', 'renderci', 'conto', 'grande', 'velocità', 'pianeta', 'muove'], ['Bill', 'Gates', 'detto', 'vaccino', 'Covid-19', '«non', 'sicuro,', 'facciamolo', 'comunque»'], ['«Perakov', 'Natalya,', 'prima', 'donna', 'pilota', 'dell’aviazione', 'ucraina,', 'trovato', 'l’altro', 'giorno', 'morte', 'cieli', 'patria.', '#stopwar»'], ['Enorme', 'ingorgo', 'ponte', 'Kerch.', 'russi', 'pronti', 'lasciare', 'Crimea,', 'dopo', 'distruzione', "dell'aeroporto", 'occupanti,', 'aumentano', 'ora', 'ora'], ['“Eni', 'bloccato', 'prezzo', 'gas', 'Russia', '10', 'anni', 'fa', 'contratto.', 'continua', 'pagarlo', 'quel', 'prezzo.', 'Però', 'applica', 'prezzo', 'determinato', 'borsa', 'Amsterdam.', 'Quindi', 'compra', '2', '(come', 'contratto)', 've', 'rivende', '30', '(grazie', 'borsa', 'pura', 'speculazione).', 'Eni', 'meccanismo', 'utile', '600', 'miliardi', 'primi', '6', 'mesi', "quest'anno.", 'Eni', 'casualmente', 'spostato', 'sede', 'legale', 'Olanda.', "L'Eni", 'compartecipata', 'statale', '30,62%', '(4', 'rotti%', 'ministero', "dell'economia", 'finanze', '26', 'rotti%', 'Cassa', 'Depositi', 'Prestiti).', 'Quindi', 'parte', "quell'utile", '(180', 'MILIARDI!!!)', 'stato', 'italiano,', 'vuole', 'ridarlo', 'clienti', '(Cittadini', 'Imprese).', 'Altro', 'sforamento', 'bilancio', 'PNNR.', 'finita', 'qui.', 'società', 'borsa', 'contratta', 'gas,', 'fatalità', 'americana.', 'Paga', '3%', 'tasse', 'Olanda', 'resto', 'porta', 'chissà', 'dove.', 'contempo', 'però', 'alzando', 'artificiosamente', 'prezzo', 'gas,', 'modo', 'paesi', 'europei', 'costretti', 'comprare', '(al', 'triplo', 'prezzo)', 'gas', 'americano', '(bontà', 'loro,', 'mossi', 'humana', 'pietas', 'ce', 'vendono).', 'vedete', 'Putin', "c'entra", 'tubo', '(scusate', 'battuta).', 'vero', 'nemico', 'Italia.', 'già', 'venuta', 'colica', '?', 'volete', 'continuo...”', 'Mario', 'Giordano'], ['«Oggi', 'aggiungiamo', 'ancora', 'confronto', 'ghiacci', 'artici.', 'Ricordate?', 'ghiaccio', "dell'Artico", 'scomparendo', 'alcuni', 'pseudoscienziati...', 'ehm...', 'oggi', "c'è", 'tanto', 'ghiaccio', 'ce', "n'era", '1989.', 'Trovate', 'differenza', 'entrambe', 'immagini...»'], ['«Vendesi', 'carri', 'armati', 'eBay', 'catturati', 'Ucraina»'], ['Muammar', 'Gheddafi:', '«Creeranno', 'virus', 'soli', 'venderanno', 'antidoti', 'poi', 'finta', 'aver', 'bisogno', 'tempo', 'trovare', 'soluzione', 'quando', 'già', 'ce', "l'hanno»"], ['«Covid', 'Pandemia', 'pilotata.', 'L’Unione', 'europea', 'sapeva.', 'Ecco', 'documenti»'], ['ministero', 'Difesa', 'ripristinato', 'leva', 'obligatoria'], ['Telepass,', 'posizionarlo', 'mai', 'così:', 'paghi', 'doppio', 'ogni', 'volta']]
clean_docs = keyword_array

title_array = [['Putin: “non accetto lezioni di democrazia da un paese che impedisce ad una parte della sua popolazione persino di prendere l’autobus per andare al lavoro”'], ['Queste auto sono state bruciate da rifugiati ucraini per motivazioni politiche legate alla guerra in Russia'], ['Stanno somministrando alle mucche il vaccino mRNA Che passerà il vaccino nel latte, nel formaggio, ecc'], 
['Le foto mostrano la folla alla manifestazione pro Trump del 14 novembre 2020'], ['Putin: “non accetto lezioni di democrazia da un paese che impedisce ad una parte della sua popolazione persino di prendere l’autobus per andare al lavoro”'], 
['Questo video della luna è stato girato al confine tra Canada, Alaska e Russia. Questo fenomeno si verifica solo nel perigeo (il punto in cui la luna è più vicina alla terra) ed è proprio qui che possiamo renderci conto della grande velocità con cui il nostro pianeta si muove'], 
['Bill Gates ha detto che il vaccino contro la Covid-19 «non sarà sicuro, ma facciamolo comunque»'], ['«Perakov Natalya, prima donna pilota dell’aviazione ucraina, ha trovato l’altro giorno la morte nei cieli della sua patria. #stopwar»'], 
["Enorme ingorgo sul ponte di Kerch. I russi pronti a lasciare la Crimea, dopo la distruzione dell'aeroporto degli occupanti, aumentano di ora in ora"], ["“Eni ha bloccato il prezzo del gas con la Russia 10 anni fa con un contratto. E continua a pagarlo a quel prezzo. Però vi applica il prezzo determinato dalla borsa di Amsterdam. Quindi lo compra a 2 (come da contratto) e ve lo rivende a 30 (grazie alla borsa che è pura speculazione). Eni con questo meccanismo ha avuto un utile di 600 miliardi nei primi 6 mesi di quest'anno. Eni casualmente ha spostato la sede legale in Olanda. L'Eni è una compartecipata statale al 30,62% (4 e rotti% ministero dell'economia e finanze e 26 e rotti% Cassa Depositi e Prestiti). Quindi parte di quell'utile (180 MILIARDI!!!) è dello stato italiano, che non vuole ridarlo ai clienti (Cittadini e Imprese). Altro che sforamento di bilancio e PNNR. Non è finita qui. La società che in borsa contratta il gas, fatalità è americana. Paga il 3% di tasse in Olanda e il resto lo porta chissà dove. Nel contempo però sta alzando artificiosamente il prezzo del gas, in modo che i paesi europei siano costretti a comprare (al triplo del prezzo) il gas americano (bontà loro, che mossi da humana pietas ce lo vendono). Come vedete Putin non c'entra un tubo (scusate la battuta). Il vero nemico è in Italia. Vi è già venuta una colica ? Se volete continuo...” Mario Giordano"], 
["«Oggi aggiungiamo ancora un confronto tra i ghiacci artici. Ricordate? Il ghiaccio dell'Artico stava scomparendo per alcuni pseudoscienziati... ehm... oggi c'è tanto ghiaccio quanto ce n'era nel 1989. Trovate la differenza in entrambe le immagini...»"], 
['«Vendesi carri armati su eBay catturati in Ucraina»'], ["Muammar Gheddafi: «Creeranno virus da soli e ti venderanno antidoti e poi faranno finta di aver bisogno di tempo per trovare una soluzione quando già ce l'hanno»"], ['«Covid e la Pandemia pilotata. L’Unione europea sapeva. Ecco i documenti»'], ['Il ministero della Difesa ha ripristinato la leva obligatoria'], ['Telepass, non posizionarlo mai così: paghi il doppio ogni volta']]



# plot one wordcloud for topics
def plot_word_cloud(number_of_topics, doc_term_matrix, dictionary):

  lsa_model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary) # train model


  # subplot for every topic

  i = 1
  for topic_i,words_and_importance in lsa_model.print_topics(num_topics=number_of_topics, num_words=10):
    print("TOPIC:",topic_i)
    
    word_wordcloud = ''
    for app in words_and_importance.split(" + "):
      value,token = app.split("*")
      value = float(value)
      token = str(token.replace('"',""))
      word_wordcloud += token # wordcloud take a string
      print("\t",value,token)
    print()
    
    wordcloud = WordCloud(background_color="white", max_words=30).generate(word_wordcloud)
    plt.subplot(4, 4, i )
    plt.imshow(wordcloud)
    plt.axis("off")

    i += 1

# return number of optimal topics and a matrix and dictionary used for plot word cloud
def lda(data, debug=False):

  #number_of_topics = 6

  #clean_docs = [['aprile', 'auto', 'Hannover', '2022', 'polizia', 'pubblicato', 'mostra', 'serie', 'bruciate', 'state'], ['vaccino', 'animali', 'ottobre', '2022', 'Nuovo', 'Galles', 'governo', 'vaccini', 'bestiame', 'Dna']]
  clean_docs = data

  # Creating the term dictionary of our courpus, where every unique term is assigned an index.
  dictionary = corpora.Dictionary(clean_docs)

  # Converting list of documents (corpus) into Document Term Matrix using dictionary.
  doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_docs]

  coherence_values = []

  possible_numbers_of_topics = [2,3,4,5,6,8,10,12,15,20,25,30]
  #possible_numbers_of_topics = [1,2,3,4,5,6,7]

  print(doc_term_matrix)
  print(dictionary)

  val_max = 0
  ind_max = 0
  index = 0
  for number_of_topics in possible_numbers_of_topics:
    #print("LSA for #topics:",number_of_topics)
    lsa_model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary) # train model



    coherence_model = CoherenceModel(model=lsa_model, texts=clean_docs, dictionary=dictionary, coherence='c_v')
    coherence_values.append(coherence_model.get_coherence())

    if index >= 4:
      ind_max = 4


    if coherence_values[index] > coherence_values[ind_max] and ind_max !=0:
      ind_max = index
      val_max = coherence_values[index]

    index += 1

  if debug == True:
    print(coherence_values)
    print("max_index: " + str(ind_max))
    print("value: " + str(coherence_values[ind_max]))
    print("n_topics: " + str(possible_numbers_of_topics[ind_max]))
    print(possible_numbers_of_topics)
    print(coherence_values) 
  
    plt.plot(possible_numbers_of_topics, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("Coherence values"), loc='best')
    plt.show()
  
    return possible_numbers_of_topics[ind_max], dictionary, doc_term_matrix


#n_topics, lda_dict, lda_term_matrix = lda(keyword_array, True)
#plot_word_cloud(n_topics, lda_term_matrix, lda_dict)
#plot_all(keyword_array)
