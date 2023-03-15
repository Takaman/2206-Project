from django.shortcuts import render
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import joblib
import nltk
import spacy
import logging
import tempfile
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')

log = logging.getLogger(__name__)
stopwords = set(stopwords.words('english'))

def extract(request):
    if request.method == 'POST':
        query = json.loads(request.body)['query']
        doc = nlp(query)
        tokens = []
        for token in doc:
            # exclude stopwords and punctuations
            if not token.is_stop and not token.is_punct:
                tokens.append(token.lemma_)
        token_string = ' '.join(tokens)
        return JsonResponse({'tokens': token_string}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'})

def extract_features(article_text):
    # Tokenize the text
    tokens = nlp(article_text)

    # Remove stop words and punctuation
    clean_tokens = []
    for token in tokens:
        if not token.is_stop and not token.is_punct:
            clean_tokens.append(token.lemma_)
    
    # Join the tokens into a single string
    return " ".join(clean_tokens)


clf = DecisionTreeClassifier()
vectorizer = TfidfVectorizer()
article_texts = []

def addArticleText(request):
    global article_texts
    if request.method == 'POST':
        article_text = json.loads(request.body)['articleText']
        article_texts.append(article_text)
        log.info(article_texts)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

#Do this later
def train(request):

    if request.method == 'POST':
        # Get the article texts from the POST request

        article_texts = json.loads(request.body)['articleText']
        article_text.append(article_texts)
        log.info(article_texts)

        # Vectorize the cleaned text strings using a TF-IDF vectorizer

        X = vectorizer.fit_transform(article_texts)

        # Train a decision tree classifier on the vectorized texts
        y = [1] * len(article_texts)  # Label all articles as true
        clf.fit(X, y)


        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'success': False})
    
# def train(request):
#     if request.method == 'POST':
#         articles = json.loads(request.body)['articles']

#         filename = "data.txt"

#         # Write the extracted features and labels for each article to the file
#         with open(filename, 'w') as f:
#             for article in articles:
#                 features = extract_features(article['text'])
#                 label = article['label']
#                 f.write(f"{label}\t{' '.join(features)}\n")
#         # train the model

#         # Load the data from the temporary file
#         with open(f.name, 'r') as f:
#             data = f.readlines()
        
#         # Split the data into features and labels
#         labels = []
#         features = []
#         for line in data:
#             label, text = line.strip().split('\t')
#             labels.append(label)
#             features.append(text)



#         return JsonResponse({'success': 'Model trained successfully!'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'})


def analyze(request):
    if request.method == 'POST':
        text = json.loads(request.body)['text']
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(text)
        return JsonResponse(score)
    else:
        return JsonResponse({'error': 'Invalid request method'})
