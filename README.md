# Image-Caption-Generator


----
## Description
This repository contains files related to my project on Image Caption Generation.

----
## Dataset
1. Flickr30k Dataset has been used for the training of model.
   [Flickr30K](https://www.kaggle.com/hsankesara/flickr-image-dataset)
2. Glove6B dataset [Link](https://drive.google.com/open?id=1GI5sWeCxgJEgToeVmakL69oDlXowXGU4)
----
## Requirements
* Python 3.5
* Matplotlib
* Pandas
* Numpy
* PIL 
* Tkinter
* keras
* tensorflow

## Project Structure
----
   ├── beamsearch.py <br>
   ├── clean_captions.py
   ├── Dataset
   ├── Glove
   │   └── glove.6B.300d.txt
   ├── GreedyCaption.py
   ├── gui.py
   ├── gui_sub.py
   ├── ImageFeature_extraction.py
   ├── images
   │   ├── 101654506_8eb26cfb60.jpg
   │   ├── 102455176_5f8ead62d5.jpg
   │   ├── 106490881_5a2dd9b7bd.jpg
   │   ├── 10815824_2997e03d76.jpg
   │   ├── 20190908_182047.jpeg
   │   ├── 20190908_185519.jpeg
   │   ├── 47870024_73a4481f7d.jpg
   │   ├── 56494233_1824005879.jpg
   │   └── pic.jpeg
   ├── index.jpeg
   ├── model_weights
   │   └── FinalModel.h5
   ├── Preprocessed Data
   │   ├── clean_captions.pkl
   │   ├── Image_features.pkl
   │   └── vocabulary.pkl
   ├── requirements.txt
   ├── requirements.txt~
   ├── training.py
   ├── training.py~
   ├── Untitled.ipynb
   └── vocabulary.py



## Installation
* Run the ipython notebook in jupyter notebook
    ```
    jupyter notebook
    ```

## Author

