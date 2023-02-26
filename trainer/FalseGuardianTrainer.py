import os
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


# Load the fake news dataset
fake_dataset = pd.read_csv('../datasets/Fake.csv')

# Load the true news dataset
true_dataset = pd.read_csv('../datasets/True.csv')

# Combine the datasets and create labels
fake_dataset['label'] = 0
true_dataset['label'] = 1
dataset = pd.concat([fake_dataset, true_dataset], ignore_index=True)
X = dataset['text']
y = dataset['label']

# Split the data into training and testing sets
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Tokenize the data
tokenizer = tf.keras.preprocessing.text.Tokenizer(
    num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

# Pad the sequences
max_length = max([len(seq) for seq in X_train])
X_train = tf.keras.preprocessing.sequence.pad_sequences(
    X_train, maxlen=max_length, padding='post', truncating='post')
X_test = tf.keras.preprocessing.sequence.pad_sequences(
    X_test, maxlen=max_length, padding='post', truncating='post')

# Build or load the model
if os.path.exists('FalseGuardian.h5'):
    model = tf.keras.models.load_model('FalseGuardian.h5')
    # Train the model
    model.fit(X_train, y_train, epochs=1, validation_data=(X_test, y_test))
    # Save the model
    model.save('FalseGuardian.h5')
else:
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=10000, output_dim=16, input_length=max_length),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(units=16, activation='relu'),
        tf.keras.layers.Dense(units=1, activation='sigmoid')
    ])
    # Compile the model
    model.compile(loss='binary_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    # Train the model
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
    # Save the model
    model.save('FalseGuardian.h5')

# Evaluate the model
test_loss, test_acc = model.evaluate(X_test, y_test)
print('Test Loss:', test_loss)
print('Test Accuracy:', test_acc)
