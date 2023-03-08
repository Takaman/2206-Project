from django.shortcuts import render
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import nltk
import spacy
from nltk.tokenize import word_tokenize

nlp = spacy.load("en_core_web_sm")

def extract(request):
    if request.method == 'POST':
        query = json.loads(request.body)['query']
        doc = nlp(query)
        tokens = []
        for token in doc:
            # exclude stopwords and punctuations
            if not token.is_stop and not token.is_punct:
                tokens.append(token.lemma_)
        return JsonResponse(' '.join(tokens), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'})



def analyze(request):
    if request.method == 'POST':
        text = json.loads(request.body)['text']
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(text)
        return JsonResponse(score)
    else:
        return JsonResponse({'error': 'Invalid request method'})
