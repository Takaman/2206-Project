import json
from datasets import load_dataset, Dataset
from transformers import GPT2Tokenizer
from transformers import GPT2ForSequenceClassification, Trainer, TrainingArguments
import torch
from torch import nn
from transformers import GPT2LMHeadModel, GPT2Config, Trainer, TrainingArguments

def process_fever_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data = {"text": [], "label": []}
    for line in lines:
        item = json.loads(line.strip())
        label = item["label"]
        claim = item["claim"]
        evidence = " ".join([f"[{ev[2]}]" for ev_group in item["evidence"] for ev in ev_group if ev[2] is not None])
        if label == "SUPPORTS":
            label_id = 0
        elif label == "REFUTES":
            label_id = 1
        else:
            label_id = 2
        data["text"].append(f"{claim} {evidence}")
        data["label"].append(label_id)
    return data

train_data = process_fever_data("train.jsonl")
val_data = process_fever_data("dev.jsonl")

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

