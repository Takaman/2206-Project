import json
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
import jsonlines


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



def preprocess_fever_dataset(input_file, output_file, wiki_dump_path):
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
            print(f"Label: {label}\nClaim: {claim}\nEvidence: {evidence_text}\n")
            f_out.write(f"Claim: {claim}\nEvidence: {evidence_text}\nLabel: {label}\n\n")


input_file = "train.jsonl"
output_file = "train_preprocessed.txt"
wiki_dump_path = "wiki-pages"  # Replace with the path to your Wikipedia dump
preprocess_fever_dataset(input_file, output_file, wiki_dump_path)

def fine_tune_gpt2(input_file, output_dir, epochs=3, batch_size=4):
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    config = GPT2Config.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name, config=config)

    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=input_file,
        block_size=128
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        save_steps=10_000,
        save_total_limit=1,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )
    trainer.train()

input_file = "train_preprocessed.txt"
output_dir = "finetuned_gpt2_fever"
fine_tune_gpt2(input_file, output_dir)
