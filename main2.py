import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
mapping_data = pd.read_csv(r"C:\Users\janna\Desktop\me\data.csv",dtype="str")

new_data = pd.read_csv(r"C:\Users\janna\Desktop\me\transinfo.csv",dtype="str")
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(mapping_data['Keywords'])
y = mapping_data['Category']

classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X, y)
X_new = tfidf_vectorizer.transform(new_data['transaction_info'])
predicted_categories = classifier.predict(X_new)
new_data['Predicted_Category'] = predicted_categories
for index, row in new_data.iterrows():
    print(f"{row['transaction_info']: <50}{row['Predicted_Category']}")

new_data.to_csv('classified_new_data.csv', index=False)

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score

mapping_data = pd.read_csv(r"C:\Users\janna\Desktop\me\data.csv",dtype="str")

new_data = pd.read_csv(r"C:\Users\janna\Desktop\me\transinfo.csv",dtype="str")
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(mapping_data['Keywords'])
y = mapping_data['Category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy}")
print(f"F1 Score: {f1}")
print(f"Recall: {recall}")
