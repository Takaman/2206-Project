import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load TfidfVectorizer object
tfidf = joblib.load('tfidf_vectorizer.joblib')

# Create a dataframe with a single row containing the text to classify
text = "Exclusive: Tencent is abandoning plans to venture into virtual reality hardware, as a sobering economic outlook prompts the Chinese tech giant to cut costs and headcount at its metaverse unit"
df = pd.DataFrame({'text': [text]})

# Preprocess the text using the loaded TfidfVectorizer object
X_tfidf = tfidf.transform(df['text'])

# Load XGBClassifier model
xgb = joblib.load('xgb_model.joblib')

# Make predictions on the data
y_prob = xgb.predict_proba(X_tfidf)

# Get the probability of class 1, which is real news.
prob_1 = y_prob[:, 1]
# prob_1 = y_prob[0][0]


# Print the probability of class 1 for each instance
print('Probability of class 1:\n', prob_1)

# # Make predictions on the data
y_pred = xgb.predict(X_tfidf)

print('Predicted label:', y_pred[0])
