import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# Load the test dataset
test_dataset = pd.read_csv('../datasets/True.csv')

# Load the saved model
model = tf.keras.models.load_model('FalseGuardian.h5')

# Preprocess the data
tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(test_dataset['text'])
X_test = tokenizer.texts_to_sequences(test_dataset['text'])
max_length = 8375
X_test = pad_sequences(X_test, maxlen=max_length,
                       padding='post', truncating='post')

# Make predictions
y_pred = model.predict(X_test)

# Convert predictions to labels (0 = fake, 1 = true)
y_pred_labels = [int(round(pred[0])) for pred in y_pred]

# Add predicted labels to the test dataset
test_dataset['label'] = y_pred_labels

# Save the predicted labels to a CSV file
test_dataset.to_csv('test_predictions.csv', index=False)

for i in range(len(test_dataset)):
    #print(f"Text: {test_dataset.iloc[i]['text']}")
    print(f"Predicted label: {'Fake' if y_pred_labels[i] == 0 else 'True'}\n")
