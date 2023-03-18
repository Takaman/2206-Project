import jsonlines
from datasets import load_dataset, Dataset
from transformers import GPT2Tokenizer
from transformers import GPT2ForSequenceClassification, Trainer, TrainingArguments
import torch
import glob
import os
from torch import nn
from transformers import GPT2LMHeadModel, GPT2Config, Trainer, TrainingArguments
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

model_folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(model_folder, "finetuned_gpt2_fever", "checkpoint-30000")
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


def get_wikipedia_sentence(wiki_data, page_title, sentence_id):
    if page_title in wiki_data:
        lines = wiki_data[page_title]['lines'].split('\n')
        for line in lines:
            if line.startswith(f"{sentence_id}\t"):
                return line.split('\t', 1)[1].strip()
    return None

def load_wiki_json(wiki_dump_path, file_id):
    file_name = f"{wiki_dump_path}/wiki-{file_id:03d}.jsonl"
    wiki_data = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)
            wiki_data[entry['id']] = entry
    return wiki_data

def preprocess_fever_dataset(input_file, output_file, wiki_dump_path, include_label=True):
    # Load all wiki JSON files into a dictionary
    wiki_data = {}
    for i in range(1, 110):  # Assuming there are 109 wiki JSON files
        wiki_data.update(load_wiki_json(wiki_dump_path, i))

    with open(input_file, 'r') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            example = json.loads(line)
            claim = example['claim']
            label = example['label']

            if label == "NOT ENOUGH INFO":
                continue

            evidence_sentences = []
            for evidence_set in example['evidence']:
                for evidence in evidence_set:
                    page_title = evidence[2]
                    sentence_id = evidence[3]
                    # Load the corresponding sentence from the Wikipedia dump
                    sentence = get_wikipedia_sentence(wiki_data, page_title, sentence_id)
                    if sentence:
                        evidence_sentences.append(sentence)

            evidence_text = ' '.join(evidence_sentences)
            f_out.write(f"Claim: {claim}\nEvidence: {evidence_text}\n")
            if include_label:
                f_out.write(f"Label: {label}\n")
            f_out.write("\n")


def load_preprocessed_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def generate_prediction(claim, combined_article_text):
    input_text = "Claim: " + claim + " [SEP] " + "Evidence: " + combined_article_text + " [SEP] " + "Label:"
    input_tokens = tokenizer.encode(input_text, return_tensors="pt")

    # Truncate input_tokens to fit within the model's maximum sequence length
    max_length = model.config.n_positions
    if len(input_tokens[0]) > max_length:
        input_tokens = input_tokens[:, :max_length]

    # Generate the output
    output = model.generate(input_tokens, max_length=1024, num_return_sequences=1)
    prediction = tokenizer.decode(output[0])

    # Extract the label from the generated output
    label = prediction.split("Label:")[1].strip()

    if len(split_prediction) > 1:
        label = split_prediction[1].strip()
    else:
        label = "NOT ENOUGH INFO"  # Set a default value if the label is not found
        
    if "SUPPORTS" in label:
        answer = "SUPPORTS"
    elif "REFUTES" in label:
        answer = "REFUTES"
    else:
        answer = "NOT ENOUGH INFO"

    return answer


def test_model(test_data):
    y_true = []
    y_pred = []

    for example in test_data:
        claim = example['claim']
        evidence_text = example['evidence']
        true_label = example['label']

        predicted_label = generate_prediction(claim, evidence_text)

        y_true.append(true_label)
        y_pred.append(predicted_label)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')

    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-score: {f1}")


# Preprocess the test dataset
input_file = "paper_test.jsonl"
output_file = "test_preprocessed.txt"
wiki_dump_path = "wiki-pages"  # Replace with the path to your Wikipedia dump
preprocess_fever_dataset(input_file, output_file, wiki_dump_path, include_label=False)

# Load preprocessed test data
test_data = load_preprocessed_data(output_file)

# Test your model on the preprocessed test data
test_model(test_data)