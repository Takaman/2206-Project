#This preprocesses data

import nltk
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re  



def preprocess_text(text):
    #remove special characters and digits
    text = re.sub("(\\d|\\W)+"," ",text)
    return text


Df_pd = pd.read_csv("Fake.csv",encoding = 'utf-8', header = None)

#preprocess the text data
Df_pd[1] = Df_pd[1].apply(preprocess_text)

#SAVE THE PREPROCESSED DATA
Df_pd.to_csv("preprocessed.csv", index = False, header = False)