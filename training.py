import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import string
import os
from PIL import Image
import pickle
from pickle import dump, load
from time import time
from keras.preprocessing import sequence
from keras.layers import LSTM, Embedding, TimeDistributed, Dense, RepeatVector,Activation, Flatten, Reshape, concatenate, Dropout, BatchNormalization
from keras.optimizers import Adam, RMSprop
from keras.layers.wrappers import Bidirectional
from keras.layers.merge import add
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras import Input, layers
from keras import optimizers
from keras.applications.inception_v3 import preprocess_input 
from keras.preprocessing.sequence import pad_sequences 
from keras.utils import to_categorical
#import pydot
#from IPython.display import SVG
#from keras.utils import plot_model
#from keras.utils.vis_utils import model_to_dot

vocabulary = pickle.load(open("Preprocessed Data/vocabulary.pkl", "rb")) 
captions = pickle.load(open('./Preprocessed Data/clean_captions.pkl','rb'))
image_features = pickle.load(open('./Preprocessed Data/Image_features.pkl','rb'))
print(len(image_features))
max_len =71
#word<--->index mappng
word2index={}
index2word={}
index=1
for word in vocabulary:
    word2index[word]=index
    index2word[index]=word
    index+=1

vocab_size=len(word2index)+1



def data_generator(captions,image_features,word2index,max_len,photos_per_batch):
  X1,X2,y = list(),list(),list()
  #print("len image:",len(image_features))
  #print("len caption:",len(captions))
  n=0
  while 1 :
    for key,caps in captions.items():
      n+=1
      #image feature
      feature=image_features[key] 
      #print(feature)
      for caption in caps:
        #encoding caption into inger sequence
        seq =[word2index[word] for word in caption.split() if word in word2index]
        for i in range(1,len(seq)):
          in_seq,out_seq = seq[:i],seq[i]
          in_seq = pad_sequences([in_seq],maxlen=max_len)[0]
          out_seq = to_categorical([out_seq],num_classes=vocab_size)[0]
          X1.append(feature)
          X2.append(in_seq)
          y.append(out_seq)
      # yield the batch data
      if n==photos_per_batch:
        yield [[np.array(X1),np.array(X2)],np.array(y)]
        X1,X2,y = list(),list(),list()
        n=0    


# Load Glove vectors
glove_dir = 'Glove'
embeddings_index = {} 
f = open(os.path.join(glove_dir, 'glove.6B.300d.txt'), encoding="utf-8")

for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Found %s word vectors.' % len(embeddings_index))

embedding_dim = 300

# Get 200-dim dense vector for each of the 10000 words in out vocabulary
embedding_matrix = np.zeros((vocab_size, embedding_dim))

for word, i in word2index.items():
    #if i < max_words:
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        # Words not found in the embedding index will be all zeros
        embedding_matrix[i] = embedding_vector


def create_model():
    #input of image features
    X1 = Input(shape=(2048,))
    fe1 = Dropout(0.5)(X1)
    fe2 = Dense(256,activation='relu')(fe1)
    #input of caption sequence
    X2 = Input(shape=(max_len,))
    embedding = Embedding(vocab_size,embedding_dim,mask_zero=True)(X2)
    se1 = Dropout(0.5)(embedding)
    se2 = LSTM(256)(se1)
  
    X = add([fe2,se2])
    X = Dense(256,activation='relu')(X)
  
    output = Dense(vocab_size,activation='softmax')(X)
    model = Model(inputs=[X1,X2],outputs=output)
  
    return model

model = create_model()
print("Summary of Model")
print(model.summary())

# #model Architecture
# plot_model(model, to_file='model.png')
# SVG(model_to_dot(model).create(prog='dot', format='svg'))

#setting glove weights to embedding layer and then setting it to trainable false
model.layers[2].set_weights([embedding_matrix])
model.layers[2].trainable = False

model.compile(loss='categorical_crossentropy', optimizer='adam') 

print('First Training Cycle')
#First Training Cycle
epochs = 10
number_pics_per_bath = 3
steps = len(image_features)//number_pics_per_bath

for i in range(epochs):
    generator = data_generator(captions, image_features, word2index, max_len, number_pics_per_bath)
    model.fit_generator(generator, epochs=1, steps_per_epoch=steps, verbose=1)
    model.save('./model_weights/model_' + str(i) + '.h5')

#Second Training Cycle 
epochs = 20
print('Second Training Cycle')
for i in range(epochs):
    generator = data_generator(captions, image_features, word2index, max_len, number_pics_per_bath)
    model.fit_generator(generator, epochs=1, steps_per_epoch=steps, verbose=1)
    model.save('./model_weights/model_' + str(i) + '.h5')


model.optimizer.lr = 0.0001
epochs = 10
number_pics_per_bath = 6
steps = len(image_features)//number_pics_per_bath

for i in range(epochs):
    generator = data_generator(captions, image_features, word2index, max_len, number_pics_per_bath)
    model.fit_generator(generator, epochs=1, steps_per_epoch=steps, verbose=1)
model.save_weights('./model_weights/model_40.h5')
for i in range(epochs):
    generator = data_generator(captions, image_features, word2index, max_len, number_pics_per_bath)
    model.fit_generator(generator, epochs=1, steps_per_epoch=steps, verbose=1)

model.save_weights('./model_weights/model_50.h5')

model.save('./model_weights/FinalModel.h5') 
