import pandas as pd

mapping_data = pd.read_csv(r"C:\Users\janna\Desktop\me\data.csv", dtype=str)

def classify_transaction(transaction_info):
    for index, row in mapping_data.iterrows():
        if any(keyword in transaction_info for keyword in row['Keywords'].split(',')):
            return row['Category']
    return "Other"
new_data = pd.read_csv(r"C:\Users\janna\Desktop\me\neww.csv")
new_data['Predicted_Category'] = new_data['transaction_info'].apply(classify_transaction)
new_data.to_csv('classified_new_data.csv', index=False)
print("Transaction Info\t\tPredicted Category")
print("----------------------------------------------")
for index, row in new_data.iterrows():
    print(f"{row['transaction_info']:30}\t\t{row['Predicted_Category']}")

