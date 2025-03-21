import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import FraudDetection
from datetime import datetime

# Step 1: Read the CSV file
csv_file = "synthetic_fraud_data.csv"
synthetic_df = pd.read_csv(csv_file)

# Step 2: Connect to the SQLite database
engine = create_engine('sqlite:///fraud_system.db')
Session = sessionmaker(bind=engine)
session = Session()

# Step 3: Insert data into the fraud_detection table
for _, row in synthetic_df.iterrows():
    record = FraudDetection(
        transaction_id=row['transaction_id'],
        payer_id=row['payer_id'],
        payee_id=row['payee_id'],
        amount=row['amount'],
        channel=row['channel'],
        mode=row['mode'],
        bank_code=row['bank_code'],
        transaction_datetime=datetime.strptime(row['transaction_datetime'], '%Y-%m-%d %H:%M:%S'),
        is_fraud=bool(row['is_fraud']),
        detection_method="synthetic",  # Default value
        score=0.0  # Default value
    )
    session.add(record)

# Step 4: Commit the transaction
session.commit()
session.close()

print(f"Data from '{csv_file}' has been inserted into the 'fraud_detection' table.")