# importing necessary libraries and packages
import numpy as np
import string
import pickle
from pickle import load, dump

#loading preprocessed captions
captions = pickle.load(open('./Preprocessed Data/clean_captions.pkl','rb'))


#creating vocabulary of words with count threshhold 10 in caption word corpus
word_count={}
max_len=0
for key,sentences in captions.items():
    for sentence in sentences:
        words=sentence.split()
        if len(words)>max_len:
            max_len=len(words)
        for word in words:
            word_count[word]=word_count.get(word,0)+1

vocabulary =[word for word in word_count if word_count[word]>=10 ]
print("Words to vocabulary length:",len(word_count),"-->",len(vocabulary))
print("Maximum caption length is :",max_len)

with open("Preprocessed Data/vocabulary.pkl", "wb") as encoded_pickle:
    pickle.dump(vocabulary, encoded_pickle) 
