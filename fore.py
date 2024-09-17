import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import numpy as np
df = pd.read_csv(r"C:\Users\janna\Downloads\cardholder_detailsc.csv")

df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='%d-%m-%Y')
customer_transactions = df.groupby('tracking_no').agg({
    'company_name': 'first',
    'transaction_amount': 'sum',
    'transaction_date': ['min', 'max']
})
customer_transactions.columns = ['company_name', 'total_transaction_amount','first_transaction_date', 'last_transaction_date']

revenue_df = customer_transactions.reset_index()
revenue_df.columns = ['tracking_no', 'company_name', 'total_transaction_amount','first_transaction_date', 'last_transaction_date']
X = np.arange(len(revenue_df)).reshape(-1, 1)  
y = revenue_df['total_transaction_amount']
train_size = int(0.8 * len(revenue_df))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error (MAE):", mae)
store_sums = df.groupby(['tracking_no', 'store_name'])['transaction_amount'].sum().reset_index()
store_sums.columns = ['tracking_no', 'store_name', 'total_store_amount']
final_data = []

for _, customer_data in customer_transactions.iterrows():
    customer_id = customer_data.name
    customer_expenses = store_sums[store_sums['tracking_no'] == customer_id]

    for _, row in customer_expenses.iterrows():
        final_data.append([
            customer_id,
            customer_data['company_name'],
            customer_data['first_transaction_date'],
            customer_data['last_transaction_date'],
            row['store_name'],
            row['total_store_amount']
        ])
final_df = pd.DataFrame(final_data, columns=[
    'Tracking No', 'Company Name', 'Start Date', 'End Date', 'Store Name', 'Transaction Amount'
])

final_df.to_csv(r"C:\Users\janna\Downloads\customer_transactions.csv", index=False)
print(final_df.head())
