import os
import pandas as pd
import tensorflow as tf
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Embedding, LSTM
from pathlib import Path

# Create a Path object for the directory containing the datasets
data_dir = Path('../datasets')

# Load the fake news dataset
fake_dataset = pd.read_csv(data_dir / 'Fake.csv')

# Load the true news dataset
true_dataset = pd.read_csv(data_dir / 'True.csv')

# Combine the datasets and create labels
fake_dataset['label'] = 0
true_dataset['label'] = 1
dataset = pd.concat([fake_dataset, true_dataset], ignore_index=True)

# Create a list of all the text
all_texts = dataset['text'].tolist()

# Write the combined dataframe to a new CSV file
output_file = data_dir / 'combined_preprocessed.csv'
dataset.to_csv(output_file, index=False)

# Load combined data
df =  pd.read_csv(data_dir / 'combined_preprocessed.csv')

# Preprocess text
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()
              and word not in stop_words]
    return ' '.join(tokens)

df['text'] = df['text'].apply(preprocess_text)

# Prepare data for model training
tokenizer = tf.keras.preprocessing.text.Tokenizer(
    num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])

# set the maximum length based on the length of the longest sentence
max_len = max(len(seq) for seq in sequences)

padded_sequences = pad_sequences(
    sequences, maxlen=max_len, padding='post', truncating='post')
labels = df['label'].astype(int)

# Build or load the model
if os.path.exists('FalseGuardian.h5'):
    model = tf.keras.models.load_model('FalseGuardian.h5')

    # Train model
    model.fit(padded_sequences, labels, epochs=3,
              batch_size=32, validation_split=0.2)
    
else:
    # Define model architecture
    model = Sequential()
    model.add(Embedding(10000, 128, input_length=max_len))
    model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(1, activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    # Train model
    model.fit(padded_sequences, labels, epochs=3,
              batch_size=32, validation_split=0.2)

# Save the model
model.save('FalseGuardian.h5')

# Evaluate the model
loss, accuracy = model.evaluate(padded_sequences, labels)
print(f'Test loss: {loss}')
print(f'Test accuracy: {accuracy}')
