import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
import joblib

# Load data
fake = pd.read_csv('datasets/fake.csv')
true = pd.read_csv('datasets/true.csv')

# Select relevant columns
fake = fake[['text']]
true = true[['text']]

# Add label column
fake['label'] = 0
true['label'] = 1

# Concatenate data
data = pd.concat([fake, true], ignore_index=True)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[['text']], data['label'], test_size=0.2, random_state=42)

# Create a TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')

# Fit and transform the training data
X_train_tfidf = tfidf.fit_transform(X_train['text'])

# Save the TfidfVectorizer object to a file
joblib.dump(tfidf, 'tfidf_vectorizer.joblib')

# Define the parameter grid for grid search
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.1, 0.01],
    'n_estimators': [100, 500, 1000]
}

# Use GridSearchCV to find the best hyperparameters
xgb = XGBClassifier()
grid_search = GridSearchCV(xgb, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_tfidf, y_train)

# Print the best hyperparameters
print("Best parameters: ", grid_search.best_params_)

# Use the best hyperparameters to fit the model
xgb = XGBClassifier(max_depth=grid_search.best_params_['max_depth'],
                    learning_rate=grid_search.best_params_['learning_rate'],
                    n_estimators=grid_search.best_params_['n_estimators'])
xgb.fit(X_train_tfidf, y_train)

# Save the model to a file
joblib.dump(xgb, 'xgb_model.joblib')

# Transform the test data
X_test_tfidf = tfidf.transform(X_test['text'])

# Make predictions on the test data
y_pred = xgb.predict(X_test_tfidf)

# Evaluate the model's accuracy
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy: {:.2f}%'.format(accuracy*100))

# Print the confusion matrix and classification report
cm = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:\n', cm)
cr = classification_report(y_test, y_pred)
print('Classification Report:\n', cr)
