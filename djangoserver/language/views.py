from django.shortcuts import render
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import joblib
import torch
import torch
import re
import os
import os
import nltk
import spacy
import logging
from datasets import Dataset
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import BartTokenizer, BartForConditionalGeneration
from fact_checking import FactChecker

#Load tokenizer and model
model_folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(model_folder, "finetuned_gpt2_fever", "checkpoint-30000")

model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Load the BART summarization model and tokenizer
summarization_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
summarization_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')

log = logging.getLogger(__name__)
stopwords = set(stopwords.words('english'))

def clean_article_text(text):
    #Remove HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    text_no_html = soup.get_text()

    #Remove special characters and escape sequences
    text_cleaned = re.sub(r'[\n\r\t\xa0]', ' ', text_no_html)
    return text_cleaned

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


article_texts = []

def addArticleText(request):
    global article_texts
    if request.method == 'POST':
        article_text = json.loads(request.body)['articleText']
        cleaned_article_text = clean_article_text(article_text)
        article_texts.append(cleaned_article_text)
        return JsonResponse({'Success in appending for more research': True})
    else:
        return JsonResponse({'success': False})
    

def analyze(request):
    if request.method == 'POST':
        text = json.loads(request.body)['text']
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(text)
        return JsonResponse(score)
    else:
        return JsonResponse({'error': 'Invalid request method'})

def summarize_text(text, max_length=600):
    inputs = summarization_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = summarization_model.generate(inputs, max_length=max_length, num_beams=4, length_penalty=2.0, early_stopping=True)
    summary = summarization_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def generate_prediction(claim, combined_article_text):
 
    input_text = "Claim: "+ claim + " [SEP] " +"Evidence: "+ combined_article_text + " [SEP] " + "Label:"
    input_tokens = tokenizer.encode(input_text, return_tensors="pt")

    # Truncate input_tokens to fit within the model's maximum sequence length
    max_length = model.config.n_positions
    if len(input_tokens[0]) > max_length:
        input_tokens = input_tokens[:, :max_length]

    # Generate the output
    output = model.generate(input_tokens, max_length=500, num_return_sequences=1)
    prediction = tokenizer.decode(output[0])

    # Extract the label from the generated output
    log.info("Prediction:" + prediction)
    label = prediction.split("Label:")[-1].strip()

    log.info(label)

    if "SUPPORTS" in prediction:
        answer = "TRUE"
    elif "REFUTES" in prediction:
        answer = "FALSE"
    else:
        answer = "NOT ENOUGH INFO"
    return answer



def train(request):
    combined_article_text = " ".join(article_texts)
    combined_article_text = summarize_text(combined_article_text)
    log.info(combined_article_text)
    if request.method == "POST":
        claim = json.loads(request.body)['query']
        # claim = request.POST.get("query")
        probabilities = generate_prediction(claim, combined_article_text)


        return JsonResponse({"Result": probabilities})
    else:
        return JsonResponse({"error": "Invalid request method"})