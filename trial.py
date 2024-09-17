import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Load the mapping data
mapping_data = pd.read_csv(r"C:\Users\janna\Desktop\me\data.csv", dtype="str")

# Attempt to read the transaction info data
try:
    transinfo_data = pd.read_csv(r"C:\Users\janna\Desktop\me\gift central card loc.csv", dtype="str")
except:
    transinfo_data = pd.read_csv(r"C:\Users\janna\Desktop\me\gift central card loc.csv", dtype="str")

# Display the first few rows and the columns of the data to inspect
print(transinfo_data.head())
print(transinfo_data.columns)

# Ensure the 'transaction_info' column exists, if not add it with empty strings
if 'transaction_info' not in transinfo_data.columns:
    print("Column 'transaction_info' not found in the data. Adding a dummy column.")
    transinfo_data['transaction_info'] = ''

# Fill missing values in the 'transaction_info' column
transinfo_data['transaction_info'] = transinfo_data['transaction_info'].fillna('')

# Process the mapping data
mapping_data['Keywords'] = mapping_data['Keywords'].fillna('')

# Perform TF-IDF vectorization and prediction
tfidf_vectorizer = TfidfVectorizer()
X = tfidf_vectorizer.fit_transform(mapping_data['Keywords'])
y = mapping_data['Category']

# Train the classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X, y)

# Transform the new data and predict categories
X_new = tfidf_vectorizer.transform(transinfo_data['transaction_info'])
predicted_categories = classifier.predict(X_new)

# Add the predictions to the DataFrame
transinfo_data['Predicted_Category'] = predicted_categories

# Save the results to a new CSV file
output_file = r"C:\Users\janna\Desktop\me\gift central card loc.csv"
transinfo_data.to_csv(output_file, index=False)

# Plot the distribution of predicted categories
category_counts = transinfo_data['Predicted_Category'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Predicted Categories')
plt.axis('equal')
plt.show()

print(f"Processed data saved to {output_file}")
