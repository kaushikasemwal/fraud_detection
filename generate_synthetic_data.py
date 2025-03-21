import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker for synthetic data generation
fake = Faker()

# Define the number of records
num_records = 5000

# Generate synthetic data
data = {
    "transaction_id": [fake.uuid4() for _ in range(num_records)],
    "payer_id": [fake.uuid4() for _ in range(num_records)],
    "payee_id": [fake.uuid4() for _ in range(num_records)],
    "amount": np.random.uniform(5, 5000, num_records),
    "channel": np.random.choice(["Online", "POS", "Mobile", "ATM"], num_records),
    "mode": np.random.choice(["Credit Card", "Debit Card", "UPI", "Net Banking"], num_records),
    "bank_code": np.random.choice(["Bank A", "Bank B", "Bank C", "Bank D"], num_records),
    "transaction_datetime": pd.date_range(start="2024-01-01", periods=num_records, freq='H').astype(str),
    "is_fraud": np.random.choice([0, 1], num_records, p=[0.95, 0.05])  # 5% fraud transactions
}

# Convert to DataFrame
synthetic_df = pd.DataFrame(data)

# Save dataset to CSV
synthetic_df.to_csv("synthetic_fraud_data.csv", index=False)

# Display first few rows
print("Synthetic data saved to 'synthetic_fraud_data.csv'.")
print(synthetic_df.head())