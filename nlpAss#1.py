


#importing required Libraries
from nltk.corpus import brown
from nltk.tokenize import word_tokenize
import streamlit as st
import pandas as pd

# Loading the corpus
file = open('corpus.txt' , 'r')
data = file.read()
corpus = word_tokenize(data)
lower_case_corpus = [w.lower() for w in corpus]
vocab = set(lower_case_corpus)


# Objects Needed
bigram_counts = {}
trigram_counts = {}
unigram_counts = {}


# Sliding through corpus to get unigram , bigram and trigram counts
for i in range(len(lower_case_corpus) - 2):
    # Getting bigram and trigram at each slide
    unigram = lower_case_corpus[i]
    bigram = (lower_case_corpus[i], lower_case_corpus[i+1])
    trigram = (lower_case_corpus[i], lower_case_corpus[i+1], lower_case_corpus[i+2])
    


    # Keeping track of the unigram counts
    if unigram in unigram_counts.keys():
        unigram_counts[unigram]+=1
    else:
        unigram_counts[unigram]=1
    # Keeping track of the bigram counts
    if bigram in bigram_counts.keys():
        bigram_counts[bigram] += 1
    else:
        bigram_counts[bigram] = 1
    
    # Keeping track of trigram counts
    if trigram in trigram_counts.keys():
        trigram_counts[trigram] += 1
    else:
        trigram_counts[trigram] = 1


def suggest_next_word(input_, bigram_counts, trigram_counts, vocab):
    # Consider the last bigram of sentence
    tokenized_input = word_tokenize(input_.lower())
    last_bigram = tokenized_input[-2:]
    vocab_probabilities = {}
    
    if len(last_bigram) >=2:
        for vocab_word in vocab:
            test_trigram = (last_bigram[0], last_bigram[1], vocab_word)
            test_bigram = (last_bigram[0], last_bigram[1])

            test_trigram_count = trigram_counts.get(test_trigram, 0)
            test_bigram_count = bigram_counts.get(test_bigram, 0)
            
            if test_bigram_count!=0:
                probability = test_trigram_count / test_bigram_count
                vocab_probabilities[vocab_word] = probability
    else:
        for vocab_word in vocab:
        
            test_bigram = (last_bigram[0], vocab_word)
            test_unigram = (last_bigram[0])

            test_bigram_count = bigram_counts.get(test_bigram, 0)
            test_unigram_count = unigram_counts.get(test_unigram, 0)
            
            
            if test_unigram_count!=0:
                probability = test_bigram_count / test_unigram_count
                vocab_probabilities[vocab_word] = probability
          
    # Sorting the vocab probability in descending order to get top probable words
    top_suggestions = sorted(vocab_probabilities.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_suggestions


def submit():
    if title != "":
        sulist  = suggest_next_word(title, bigram_counts, trigram_counts, vocab)
        print(sulist)
        for i in sulist:
            if(i[1]>0.0):
                st.write(title+"  "+i[0])

st.write("Here's our first attempt at using data to create a table:")
title = st.text_input('Word Search', '' , on_change=(submit))
