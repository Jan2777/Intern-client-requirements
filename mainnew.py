import pandas as pd
import re

# Load the CSV files
csv1 = pd.read_csv(r"C:\Users\janna\Desktop\me\gift central plus.csv")
csv2 = pd.read_csv(r"C:\Users\janna\Desktop\me\healthcard.csv")
csv3 = pd.read_csv(r"C:\Users\janna\Desktop\me\cashcentralplus.csv")
main_csv = pd.read_csv(r"C:\Users\janna\Desktop\me\transinfo.csv")

# Combine all transaction info into a single DataFrame
combined_df = pd.concat([csv1[['transaction_info']], csv2[['transaction_info']], csv3[['transaction_info']]])

# Remove duplicates from the combined DataFrame
unique_transactions = combined_df.drop_duplicates().reset_index(drop=True)

# Function to extract the matching pattern (first two words and last word)
def extract_pattern(transaction):
    parts = transaction.split()
    if len(parts) > 2:
        pattern = f"{parts[0]} {parts[1]} {parts[-1]}"
    else:
        pattern = transaction
    return re.escape(pattern)

# Function to count matches in main CSV based on the pattern
def count_matches(transaction):
    pattern = extract_pattern(transaction)
    return sum(main_csv['transaction_info'].str.contains(pattern, case=False, na=False))

# Apply the count_matches function to each unique transaction
unique_transactions['count'] = unique_transactions['transaction_info'].apply(count_matches)

# Count the number of repeated transactions
repeated_transactions = unique_transactions[unique_transactions['count'] > 1]

# Filter out rows with zero count (no matches) or exactly one match (unique)
non_repeated_transactions = unique_transactions[unique_transactions['count'] == 0]

# Save the non-repeated transactions to a new CSV file
non_repeated_transactions.to_csv('non_repeated_transactions.csv', index=False)

# Print repeated transactions and their occurrences
repeated_count = repeated_transactions.shape[0]
print(f"Number of repeated transactions: {repeated_count}")
print("Repeated transactions and their occurrences:")
print(repeated_transactions[['transaction_info', 'count']])

print("Non-repeated transactions have been saved to non_repeated_transactions.csv")
