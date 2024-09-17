import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
transinfo_df = pd.read_csv(r"C:\Users\janna\Desktop\me\transinfo.csv")
subcat_df = pd.read_csv(r"C:\Users\janna\Desktop\me\subcat.csv")
merged_df = pd.merge(transinfo_df, subcat_df, on='Category')
vectorizer = CountVectorizer(stop_words='english', lowercase=True)
vectorizer.fit(merged_df['keywords'])
transaction_vector = vectorizer.transform(merged_df['transaction_info'])
subcat_vector = vectorizer.transform(merged_df['keywords'])
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(transaction_vector, subcat_vector)
max_similarity = similarity.max(axis=1)
merged_df['subcategory_similarity'] = max_similarity
threshold = 0.5
filtered_df = merged_df[merged_df['subcategory_similarity'] >= threshold]
print(filtered_df[['transaction_info', 'subcategory']])
filtered_df.to_csv('transinfo_with_subcategory.csv', index=False)
