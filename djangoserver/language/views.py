from django.shortcuts import render
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import joblib
import nltk
import spacy
import logging
import tempfile
from datasets import Dataset
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
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

#Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

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


clf = DecisionTreeClassifier()
vectorizer = TfidfVectorizer()
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

#Do this later
def train(request):

    if request.method == 'POST':
        # Get the article text
        log.info("Training model...")
        log.info(article_texts)     
        # Prepare dataset
        dataset = Dataset.from_dict({"text": article_texts, "label": [1] * len(article_texts)})  # assuming all articles in the list are trustworthy

        # Tokenize the dataset
        def tokenize(batch):
            return tokenizer(batch["text"], padding="max_length", truncation=True)
        
        tokenized_dataset = dataset.map(tokenize, batched=True)

        # Fine tune the model
        training_args = TrainingArguments(
            output_dir="./results",          # output directory
            num_train_epochs=1,              # total number of training epochs
            per_device_train_batch_size=16,  # batch size per device during training
            per_device_eval_batch_size=16,   # batch size for evaluation
            logging_dir='./logs',            # directory for storing logs
        )

        trainer = Trainer(
            model=model,                         # the instantiated 🤗 Transformers model to be trained
            args=training_args,                  # training arguments, defined above
            train_dataset=tokenized_dataset,        # training dataset  
        )
        trainer.train()

        #Split datasets into train and validation set
        train_dataset = tokenized_dataset["train"].shuffle(seed=42).select(range(1000))


        # Return a JSON response indicating success
        return JsonResponse({'success': True})
    else:
        # Return a JSON response indicating failure
        return JsonResponse({'success': False})
    

def analyze(request):
    if request.method == 'POST':
        text = json.loads(request.body)['text']
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(text)
        return JsonResponse(score)
    else:
        return JsonResponse({'error': 'Invalid request method'})
