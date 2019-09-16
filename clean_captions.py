import pandas as pd 
import numpy as np
import string
import pickle
from pickle import load, dump
import os

#reading caption file
file = pd.read_csv('./Dataset/results.csv',delimiter='|')

file.columns = ['image_name', 'comment_number', 'comment']
file = np.array(file) 

#caption <--> ID mapping
def caption_IDMapping(file):
  mapping=dict()
  for row in file:
    if row[0] not in mapping:
      mapping[row[0]]=list()
    mapping[row[0]].append(row[2])
    
  return mapping

captions = caption_IDMapping(file)
#selecting only those captionins whose images are available in dataset
images = os.listdir("Dataset/flickr30k_images")
keys = [k[0] for k in captions.items()]
for key in keys:
  if key not in images:
    del captions[key] 
    
    


def clean_captions(captions):
  # prepare translation table for removing punctuation
  table = str.maketrans('', '', string.punctuation)
  for key, caption_list in captions.items():
    for i in range(len(caption_list)):
      caption = caption_list[i]
      caption = caption.split()
			# convert to lower case
      caption = [word.lower() for word in caption]
			# remove punctuation from each token
      caption = [w.translate(table) for w in caption]
			# remove hanging 's' and 'a'
      caption = [word for word in caption if len(word)>1]
			# remove tokens with numbers in them
      caption = [word for word in caption if word.isalpha()]
      caption_list[i] =  'startseq ' + ' '.join(caption) + ' endseq'

clean_captions(captions)    

with open("Preprocessed Data/clean_captions.pkl", "wb") as encoded_pickle:
    pickle.dump(captions, encoded_pickle) 

print("Preprocessed Captions are succesfully stored as **clean_captions.pkl** in folder Preprocessed Data")
