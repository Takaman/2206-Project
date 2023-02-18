import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load data
data = pd.read_csv('datasets/test.csv', delimiter=';', header=None, names=['text', 'label'])


# Define a mapping for label values
label_mapping = {'0': 0, '1': 1}

# Convert label values to numeric using the mapping
data['label'] = data['label'].map(label_mapping)

# Drop rows with missing values
data.dropna(inplace=True)

# Load TfidfVectorizer object
tfidf = joblib.load('tfidf_vectorizer.joblib')

# Transform the data
X_tfidf = tfidf.transform(data['text'])

# Load XGBClassifier model
xgb = joblib.load('xgb_model.joblib')

# Make predictions on the data
y_pred = xgb.predict(X_tfidf)

# Evaluate the model's accuracy
# accuracy = accuracy_score(data['label'], y_pred)
# print('Accuracy: {:.2f}%'.format(accuracy*100))

# Compute the accuracy of the model
accuracy = (y_pred == data['label']).mean()
print('Accuracy: {:.2f}%'.format(accuracy * 100))



# Print the confusion matrix and classification report
cm = confusion_matrix(data['label'], y_pred)
print('Confusion Matrix:\n', cm)
cr = classification_report(data['label'], y_pred)
print('Classification Report:\n', cr)


