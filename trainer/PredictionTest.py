import pandas as pd
import tensorflow as tf
from pathlib import Path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the trained model
model = tf.keras.models.load_model('FalseGuardian.h5')

# Create a Path object for the directory containing the input file
data_dir = Path("../datasets/")

# Load the true news dataset
input_df = pd.read_csv(data_dir / 'Fake.csv')

# Preprocess text
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha()
              and word not in stop_words]
    return ' '.join(tokens)

input_df['text'] = input_df['text'].apply(preprocess_text)

# Tokenize and pad the input sequences
tokenizer = tf.keras.preprocessing.text.Tokenizer(
    num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(input_df['text'])
sequences = tokenizer.texts_to_sequences(input_df['text'])
max_len = model.layers[0].input_shape[1]
padded_sequences = pad_sequences(
    sequences, maxlen=max_len, padding='post', truncating='post')

# Make predictions on the input sequences
predictions = model.predict(padded_sequences)

# Set a threshold for classification
threshold = 0.5

# Convert probabilities to binary predictions based on the threshold
binary_predictions = (predictions > threshold).astype(int)

# Convert binary predictions to True or False
predicted_labels = ['True' if x == 1 else 'Fake' for x in binary_predictions]

# Print the predicted labels
print(predicted_labels)