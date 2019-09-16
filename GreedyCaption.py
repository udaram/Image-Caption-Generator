import numpy as np
import matplotlib.pyplot as plt
import pickle 
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras import Input, layers
from keras.applications.inception_v3 import preprocess_input 
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model


vocabulary = pickle.load(open("Preprocessed Data/vocabulary.pkl", "rb")) 
model = load_model('model_weights/FinalModel.h5')
max_len =71
#word<--->index mappng
word2index={}
index2word={}
index=1
for word in vocabulary:
    word2index[word]=index
    index2word[index]=word
    index+=1

def greedySearch(image_feature):
    in_text = 'startseq'
    for i in range(max_len):
        sequence = [word2index[w] for w in in_text.split() if w in word2index]
        sequence = pad_sequences([sequence], maxlen=max_len)
        predict = model.predict([image_feature,sequence], verbose=0)
        predict = np.argmax(predict)
        word = index2word[predict]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final



#pretrained CNN model
CNNmodel = InceptionV3(weights='imagenet')
CNNmodel = Model(CNNmodel.input,CNNmodel.layers[-2].output)
#print("Extracting Features of Images:Wait.....")

#preprocessing image
def preprocess_image(image_path):
    img = image.load_img(image_path,target_size=(299,299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array,axis=0)
    img_array = preprocess_input(img_array)
    return img_array 

#image feature extraction
def encode_image(image):
    img =preprocess_image(image)
    feature_vec = CNNmodel.predict(img)
    feature_vec = np.reshape(feature_vec,feature_vec.shape[1])
    return feature_vec 

def generate_caption(path):
    feature = encode_image(path).reshape((1,2048))
#x=plt.imread('images/image1.jpeg')
#plt.imshow(x)
    return str(greedySearch(feature))
