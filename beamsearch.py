
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



#pretrained CNN model
CNNmodel = InceptionV3(weights='imagenet')
CNNmodel = Model(CNNmodel.input,CNNmodel.layers[-2].output)


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

def beam_search_predictions(image, beam_index = 3):
    start = [word2index["startseq"]]
    
    start_word = [[start, 1]]
    
    while len(start_word[0][0]) < max_len:
        temp = []
        for s in start_word:
            par_caps = pad_sequences([s[0]], maxlen=max_len, padding='post')
            e = image
            preds = model.predict([np.array(e), np.array(par_caps)])
            
            # Getting the top <beam_index>(n) predictions
            word_preds = np.argsort(preds[0])[-beam_index:]
            
            # creating a new list so as to put them via the model again
            for w in word_preds:
                next_cap, prob = s[0][:], s[1]
                next_cap.append(w)
                prob += preds[0][w]
                temp.append([next_cap, prob])
                    
        start_word = temp
        # Sorting according to the probabilities
        start_word = sorted(start_word, reverse=False, key=lambda l: l[1])
        # Getting the top words
        start_word = start_word[-beam_index:]
    
    start_word = start_word[-1][0]
    intermediate_caption = [index2word[i] for i in start_word]

    final_caption = []
    
    for i in intermediate_caption:
        if i != 'endseq':
            final_caption.append(i)
        else:
            break
    
    final_caption = ' '.join(final_caption[1:])
    return final_caption
  
  
def generate_caption(file):
    feature = encode_image(file).reshape((1,2048))
#x=plt.imread('/content/drive/My Drive/30 K Image Captioning/images/102455176_5f8ead62d5.jpg')
#plt.imshow(x)
    return (str(beam_search_predictions(feature,7))) 
