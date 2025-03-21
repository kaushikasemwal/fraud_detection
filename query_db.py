from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import FraudDetection

# Connect to the database
engine = create_engine('sqlite:///fraud_system.db')
Session = sessionmaker(bind=engine)
session = Session()

# Fetch the first 10 records
records = session.query(FraudDetection).limit(10).all()
for record in records:
    print(record.transaction_id, record.amount, record.is_fraud)

session.close()