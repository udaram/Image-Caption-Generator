import numpy as np 
import matplotlib.pyplot as plt
import os
from PIL import Image
import pickle
from pickle import dump, load
from time import time
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras import Input, layers
from keras.applications.inception_v3 import preprocess_input



#pretrained CNN model
CNNmodel = InceptionV3(weights='imagenet')
CNNmodel = Model(CNNmodel.input,CNNmodel.layers[-2].output)
print("Extracting Features of Images:Wait.....")
start = time()
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

image_features={}
i=0
for image_name in os.listdir('Dataset/flickr30k_images')[:50]:
    image_path = 'Dataset/flickr30k_images/'+image_name
    i+=1
    print("image:",i,"Name:",image_name)
    image_features['image_name']=encode_image(image_path) 

print("Time taken in seconds =", time()-start)  
print("Extracting Features of Images:Finished")
#saving all image features in pickle formet
with open('Preprocessed Data/Image_features.pkl','wb') as encoded_pickle:
    pickle.dump(image_features,encoded_pickle) 