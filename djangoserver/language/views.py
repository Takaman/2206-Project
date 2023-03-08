from django.shortcuts import render
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import spacy

nlp = spacy.load("en_core_web_sm")

def extract(request):
    if request.method == 'POST':
        query = json.loads(request.body)['query']
        doc = nlp(query)
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_
            })
        
        entity_string = ', '.join([ent['text'] for ent in entities])
        return JsonResponse(entity_string, safe=False)
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
