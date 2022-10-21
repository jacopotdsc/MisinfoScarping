from gensim import corpora
from gensim.models import LsiModel
from gensim.models.coherencemodel import CoherenceModel
import matplotlib as plt

keyword_array = [['Putin', 'Draghi', '2022', 'presidente', 'dichiarazioni', 'riferimento', 'conferenza', 'stampa', '24', 'febbraio'], ['aprile', 'auto', 'Hannover', '2022', 'polizia', 'pubblicato', 'mostra', 'serie', 'bruciate', 'state'], ['vaccino', 'animali', 'ottobre', '2022', 'Nuovo', 'Galles', 'governo', 'vaccini', 'bestiame', 'Dna'], ['Telepass', 'potrebbe', 'dispositivo', 'posizionato', 'parte', 'sbarra', 'doppio', 'fatto', 'pedaggio', 'inferiore']]
title_array = [['Putin: “non accetto lezioni di democrazia da un paese che impedisce ad una parte della sua popolazione persino di prendere l’autobus per andare al lavoro”'], ['Queste auto sono state bruciate da rifugiati ucraini per motivazioni politiche legate alla guerra in Russia'], ['Stanno somministrando alle mucche il vaccino mRNA Che passerà il vaccino nel latte, nel formaggio, ecc'], ['Telepass, non posizionarlo mai così: paghi il doppio ogni volta']]



def lda(clean_docs):

  number_of_topics = 5

  # Creating the term dictionary of our courpus, where every unique term is assigned an index.
  dictionary = corpora.Dictionary(clean_docs)

  # Converting list of documents (corpus) into Document Term Matrix using dictionary.
  doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_docs]

  lsa_model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary) # train model

  for topic_i,words_and_importance in lsa_model.print_topics(num_topics=number_of_topics, num_words=10):
    #print("TOPIC:",topic_i)
    for app in words_and_importance.split(" + "):
      value,token = app.split("*")
      value = float(value)
      token = str(token.replace('"',""))
     # print("\t",value,token)
    #print()

  docs_ids = []
  for i,doc in enumerate(clean_docs):
    if "giz" in doc:
      docs_ids.append(i)
    


  coherence_values = []

  possible_numbers_of_topics = [2,3,4,5,6,8,10,12,15,20,25,30]
  #possible_numbers_of_topics = [2,3,4,5,6,8,10]
  #print(doc_term_matrix)

  for number_of_topics in possible_numbers_of_topics:
    #print("LSA for #topics:",number_of_topics)
    lsa_model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary) # train model
    
    coherence_model = CoherenceModel(model=lsa_model, texts=clean_docs, dictionary=dictionary, coherence='c_v')
    coherence_values.append(coherence_model.get_coherence())

  print(possible_numbers_of_topics)
  print(coherence_values)

  plt.plot(possible_numbers_of_topics, coherence_values)
  plt.xlabel("Number of Topics")
  plt.ylabel("Coherence score")
  plt.legend(("Coherence values"), loc='best')
  plt.show()


lda(keyword_array)