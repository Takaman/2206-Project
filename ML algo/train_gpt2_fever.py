import json
from datasets import load_dataset, Dataset
from transformers import GPT2Tokenizer
from transformers import GPT2ForSequenceClassification, Trainer, TrainingArguments
import torch
import glob
import os
from torch import nn
from transformers import GPT2LMHeadModel, GPT2Config, Trainer, TrainingArguments


def extract_wiki_data(wiki_folder_path):
    wiki_data = {}
    
    # Iterate through all the files in the wiki_folder_path
    for file_name in os.listdir(wiki_folder_path):
        file_path = os.path.join(wiki_folder_path, file_name)
        
        # Read the file and extract the necessary data
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line_data = json.loads(line)
                page_id = line_data["id"]
                text = line_data["text"]
                wiki_data[page_id] = text
                
    return wiki_data

def process_fever_data(jsonl_file, wiki_data):
    data = {"text": [], "label": []}
    
    with open(jsonl_file, "r") as file:
        for line in file:
            claim_data = json.loads(line)

            claim = claim_data["claim"]
            label = claim_data["label"]
            
            if label != "NOT ENOUGH INFO":
                evidence_text = ""
                for evidence_group in claim_data["evidence"]:
                    for evidence in evidence_group:
                        wiki_title = evidence[2]
                        sentence_id = evidence[3]
                        evidence_sentence = wiki_data.get(wiki_title, "").split("\n")[sentence_id].strip()
                        evidence_text += f" {evidence_sentence}"
                        
                text = f"{claim} [SEP] {evidence_text}"
            else:
                text = claim
                
            data["text"].append(text)
            data["label"].append(label)
            
    return data




wiki_data = extract_wiki_data("wiki-pages")
train_data = process_fever_data("train.jsonl", wiki_data)
val_data = process_fever_data("dev.jsonl", wiki_data)

train_dataset = Dataset.from_dict(train_data)
val_dataset = Dataset.from_dict(val_data)


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

def tokenize_dataset(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=512)

train_dataset = train_dataset.map(tokenize_dataset, batched=True)
val_dataset = val_dataset.map(tokenize_dataset, batched=True)
train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
val_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

class GPT2ForTextClassification(GPT2LMHeadModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.dropout = nn.Dropout(config.resid_pdrop)
        self.classifier = nn.Linear(config.n_embd, config.num_labels)
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, input_ids, attention_mask, labels):
        outputs = self.transformer(input_ids, attention_mask=attention_mask)
        logits = self.classifier(self.dropout(outputs.last_hidden_state[:, 0]))
        loss = self.loss_fn(logits, labels)
        return loss, logits

config = GPT2Config.from_pretrained("gpt2", num_labels=3)
model = GPT2ForTextClassification.from_pretrained("gpt2", config=config)
model = model.to("cuda") #Moving model to GPU

training_args = TrainingArguments(
    output_dir="gpt2_finetuned",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    evaluation_strategy="epoch",
    logging_dir="./logs",
)

def compute_metrics(predictions, labels):
    preds = predictions.argmax(-1)
    accuracy = (preds == labels).mean()
    return {"accuracy": accuracy}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.save_model("gpt2_finetuned")

